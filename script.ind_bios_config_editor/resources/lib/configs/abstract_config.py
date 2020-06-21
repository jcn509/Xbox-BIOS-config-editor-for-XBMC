"""Abstract class used to control access to config files.

It automatically validates all values and converts them between Python and
config file formats
"""
from abc import ABCMeta, abstractmethod
from collections import namedtuple
import ConfigParser
import os
import re
from StringIO import StringIO
try:
    # typing not available on XBMC4XBOX
    from typing import Any, Dict, Tuple
except:
    pass

from .config_errors import (
    ConfigError,
    ConfigFieldNameError,
    ConfigFieldValueError,
    ConfigPresetDoesNotExistError,
)
from .factories import format_converter_factory, validator_factory


class AbstractConfig(object):
    """Abstract class used to control access to config files.

    It automatically validates all values and converts them between Python and
    config file formats
    """
    __metaclass__ = ABCMeta

    def __init__(self, max_line_length=None, quote_char_if_whitespace=None):
        """quote_char_if_whitespace is the optional quote character used to
        wrap values if they contain whitespace
        """
        # type: (int, str) -> None
        fields = self._get_fields()
        self._options = tuple(field.field_name for field in fields)

        self._defaults = {field.field_name: field.default_value for field in fields}

        # pytype not callable errors are incorrect
        # pytype: disable=not-callable
        self._format_converters = {
            field.field_name: format_converter_factory(field) for field in fields
        }
        self._validators = {
            field.field_name: validator_factory(field) for field in fields
        }
        # pytype: enable=not-callable

        self._max_line_length = max_line_length
        self._quote_char_if_whitespace = quote_char_if_whitespace

        # Could inherit from RawConfigParser instead
        # but decided not as the interface is different
        # e.g. get and set take different arguments
        # and get does not always return a string.
        self._config_parser = ConfigParser.RawConfigParser()
        self._config_parser.optionxform = self._format_option_name

        for field in self._defaults:
            self.set(field, self._defaults[field])

    def defaults(self):
        """Returns a dictionary with the default value for each field

        (in Python format)
        """
        # type: () -> Dict[str, Any]
        return self._defaults

    def options(self):
        """Returns all the options that can be set in the config file"""
        # type: () -> Tuple[str, ...]
        return self._options

    @abstractmethod
    def _get_fields(self):
        """Returns a tuple containing descriptions for each field"""
        # type: () -> Tuple[Any, ...]
        pass

    @abstractmethod
    def _get_true_if_fields_dont_have_values(self):
        """Fields that should be set to True if at least one of the other
        fields they refer to does not have a certain value (and False
        otherwise)
        """
        # type: () -> Dict[str, Dict[str, Any]]
        pass

    def read(self, filename, set_invalid_fields_to_default=True, *args, **kwargs):
        """Read the config file with filename, and take the field values from
        it

        If set_invalid_fields_to_default is False an error will be thrown if
        any field has an invalid value
        """
        # type: (str, bool, Any, Any) -> None
        with open(filename) as fp:
            self.readfp(
                fp,
                set_invalid_fields_to_default=set_invalid_fields_to_default,
                *args,
                **kwargs
            )

    def _remove_start_end_quote_chars(self):
        """If values are wrapped in quote characters, remove the quote characters"""
        # type: () -> None
        if self._quote_char_if_whitespace:
            for field in self._options:
                value = self._get_in_config_file_format(field)
                if (
                    value[0] == self._quote_char_if_whitespace
                    and value[-1] == self._quote_char_if_whitespace
                ):
                    self._set_in_config_format(field, value[1:-1])

    def readfp(self, fp, set_invalid_fields_to_default=True, *args, **kwargs):
        """Read from the file pointer object, and take the field values from it
        
        If set_invalid_fields_to_default is False an error will be thrown if
        any field has an invalid value
        """
        # type: (Any, bool, Any, Any) -> None
        stream = StringIO()

        try:
            stream.name = fp.name
        except AttributeError:
            pass

        stream.write("[" + ConfigParser.DEFAULTSECT + "]\n")
        stream.write(fp.read())
        stream.seek(0, 0)

        self._config_parser.readfp(stream, *args, **kwargs)
        if self._quote_char_if_whitespace:
            self._remove_start_end_quote_chars()
        self._validate_everything_in_config_file_format(set_invalid_fields_to_default)

    def _validate_everything_in_config_file_format(
        self, set_invalid_fields_to_default=False
    ):
        """Validate option names and values in the config file format

        If set_invalid_fields_to_default is True invalid fields will be set to
        their default values otherwise an exception will be thrown for invalid
        values
        """
        # type: (bool) -> None
        for option in self.options():
            value = self._get_in_config_file_format(option)
            if set_invalid_fields_to_default:
                try:
                    self._validate_option_name_and_value(
                        option, value, value_is_in_config_format=True
                    )
                except ConfigError as e:
                    self.set_to_default(option)
            else:
                self._validate_option_name_and_value(
                    option, value, value_is_in_config_format=True
                )

    def _validate_option_name(self, option_name):
        """Throw an error if option_name does not exist for this config file"""
        if option_name not in self._options:
            raise ConfigFieldNameError(option_name + " is not a valid option")

    def _validate_config_file_line_length(self, option_name, value_in_config_format):
        """Throw an error if the line in the config file will not be too long
        """
        # type: (str, str) -> None
        if self._max_line_length is not None:
            # The equals sign, and \r\n on the end of line
            additional_chars = 3
            if self._quote_char_if_whitespace and re.search(
                r"\s", value_in_config_format
            ):
                # The quotes around the value
                additional_chars += 2
            if (
                len(option_name) + len(value_in_config_format) + additional_chars
                > self._max_line_length
            ):
                raise ConfigFieldValueError(
                    "Cannot use "
                    + value_in_config_format
                    + " for field "
                    + option_name
                    + " the line length in the file would be too long"
                )

    def _validate_option_name_and_value(
        self, option_name, value, value_is_in_config_format=False
    ):
        """Throw an exception if the option does not exist or its value is not
        valid
        
        Checks values in config format if value_is_in_config_format is True and
        in Python format otherwise
        """
        # type: (str, Any, bool) -> None
        self._validate_option_name(option_name)

        # Won't reach this if option name is invalid
        # (which is what we want as there will be no validator
        # if the option does not exist)
        validator = self._validators[option_name]
        if value_is_in_config_format:
            validator.validate_in_config_file_format(value)
            self._validate_config_file_line_length(option_name, value)
        else:
            validator.validate_in_python_format(value)

    def _format_option_name(self, option):
        """Used to convert an option name from outside the class to the format
        that is used internally

        Default implementation is to convert it to upper case
        """
        # type: (str) -> str
        return option.upper()

    def load_preset(
        self, filename, fields_to_apply_to, set_invalid_fields_to_default=True
    ):
        """Load a config file and use its values to set the values of certain
        fields in this config file.

        if set_invalid_fields_to_default is False then an exception will be
        thrown if the preset file contains any invalid field values
        """
        # type: (str, Tuple[str, ...], bool) -> None
        if not os.path.isfile(filename):
            raise ConfigPresetDoesNotExistError(
                "Preset '" + filename + "' does not exist"
            )
        # Need to disable this error as during execution self.__class__ does
        # not refer to an instance of AbstractConfig but rather an instance
        # of one of its subclasses
        preset_config = self.__class__()  # pytype: disable=not-instantiable
        preset_config.read(
            filename, set_invalid_fields_to_default=set_invalid_fields_to_default
        )

        for field in fields_to_apply_to:
            self.set(field, preset_config.get(field))

    def get(self, option, validate_option_name=True):
        """Get the value of option in Python format"""
        # type: (str, bool) ->  Any
        if validate_option_name:
            option = self._format_option_name(option)
            self._validate_option_name(option)
        value_in_config_format = self._get_in_config_file_format(option)
        format_converter = self._format_converters[option]
        return format_converter.convert_to_python_format(value_in_config_format)

    def _get_in_config_file_format(self, option):
        """Get the value of option in config file format"""
        # type: (str) -> str
        return self._config_parser.get(ConfigParser.DEFAULTSECT, option)

    def set_to_default(self, option):
        """Set the option to its default value"""
        # type: (str) -> None
        option = self._format_option_name(option)
        self.set(option, self._defaults[option])

    def set(self, option, value, validate_option_name_and_value=True):
        """Set the option to the value

        Python format must be used for the value
        """
        # type: (str, Any, bool) -> None
        if validate_option_name_and_value:
            option = self._format_option_name(option)
            self._validate_option_name_and_value(option, value)
        format_converter = self._format_converters[option]
        value_in_config_format = format_converter.convert_to_config_file_format(value)
        return self._set_in_config_format(option, value_in_config_format)

    def _set_in_config_format(self, option, value):
        """Set the option to the value. No validation is performed

        config format must be used for the value
        """
        # type: (str, str) -> None
        return self._config_parser.set(ConfigParser.DEFAULTSECT, option, value)

    def write(self, fp, dont_write_option_if_value_default=True):
        """Write the config out to the given config file

        If dont_write_option_if_value_default is True then if an option has its
        default value it won't be written to the file
        """
        # type: (Any, bool) -> None
        true_if_fields_dont_have_values = self._get_true_if_fields_dont_have_values()
        for field in true_if_fields_dont_have_values:
            value = False
            for field_to_check in true_if_fields_dont_have_values[field]:
                value_to_check_for = true_if_fields_dont_have_values[field][field_to_check]

                if self.get(field_to_check) != value_to_check_for:
                    value = True
                    break
            self.set(field, value)

        if self._quote_char_if_whitespace:
            for field in self._options:
                value = self._get_in_config_file_format(field)
                if re.search(r"\s", value):
                    value = (
                        self._quote_char_if_whitespace
                        + value
                        + self._quote_char_if_whitespace
                    )
                    self._set_in_config_format(field, value)
        
        stream = StringIO()
        if dont_write_option_if_value_default:
            output_file = ConfigParser.RawConfigParser()
            output_file.optionxform = self._format_option_name
            for field in self._options:
                if (
                    field not in self._defaults
                    or self.get(field) != self._defaults[field]
                ):
                    value_in_config_file_format = self._get_in_config_file_format(field)
                    output_file.set(
                        ConfigParser.DEFAULTSECT, field, value_in_config_file_format
                    )
            output_file.write(stream)
        else:
            self._config_parser.write(stream)

        # Ignore the first line which will be a marker for the default section
        stream.seek(0, 0)
        stream.readline()
        # Replace the first non-commented out instance of " = " with "="
        # (Some config files have line length limits)
        equals_white_space_regex = re.compile(r"^([^;]+)\s+=\s+")
        for line in stream:
            fp.write(equals_white_space_regex.sub(r"\1=", line))

        if self._quote_char_if_whitespace:
            self._remove_start_end_quote_chars()
