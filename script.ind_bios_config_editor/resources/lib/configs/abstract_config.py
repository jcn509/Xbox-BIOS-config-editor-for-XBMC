import ConfigParser
from StringIO import StringIO
import os
import re
from abc import ABCMeta, abstractmethod
from .config_errors import (
    ConfigError,
    ConfigFieldNameError,
    ConfigFieldValueError,
    ConfigPresetDoesNotExistError,
)
from .validators import validator_factory
from .format_converters import format_converter_factory


class AbstractConfig(object):
    __metaclass__ = ABCMeta

    def __init__(self, max_line_length=None, quote_char_if_whitespace=None):
        fields = self._get_fields()
        self._options = tuple(field.field_name for field in fields)

        self._defaults = {field.field_name: field.default_value for field in fields}
        self._format_converters = {
            field.field_name: format_converter_factory(field) for field in fields
        }
        self._validators = {
            field.field_name: validator_factory(field) for field in fields
        }

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
        return self._defaults

    def options(self):
        return self._options

    @abstractmethod
    def _get_fields(self):
        pass

    @abstractmethod
    def _get_true_if_non_default(self):
        pass

    @abstractmethod
    def _get_true_if_non_zero(self):
        pass

    def read(self, filename, set_invalid_fields_to_default=True, *args, **kwargs):
        with open(filename) as fp:
            self.readfp(
                fp,
                set_invalid_fields_to_default=set_invalid_fields_to_default,
                *args,
                **kwargs
            )

    def _remove_start_end_quote_chars(self):
        if self._quote_char_if_whitespace:
            for field in self._options:
                value = self._get_in_config_format(field)
                if (
                    value[0] == self._quote_char_if_whitespace
                    and value[-1] == self._quote_char_if_whitespace
                ):
                    self._set_in_config_format(field, value[1:-1])

    def readfp(self, fp, set_invalid_fields_to_default=True, *args, **kwargs):
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
        self._validate_everything_in_config_format(set_invalid_fields_to_default)

    def _validate_everything_in_config_format(
        self, set_invalid_fields_to_default=False
    ):
        for option in self.options():
            value = self._get_in_config_format(option)
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
        if option_name not in self._options:
            raise ConfigFieldNameError(option_name + " is not a valid option")

    def _validate_config_file_line_length(self, option_name, value_in_config_format):
        """Ensure that the line in the cfg file will not be too long"""
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
        self._validate_option_name(option_name)

        # Won't reach this if option name is invalid
        # (which is what we want as there will be no validator
        # if the option does not exist)
        validator = self._validators[option_name]
        if value_is_in_config_format:
            validator.validate_in_config_format(value)
            self._validate_config_file_line_length(option_name, value)
        else:
            validator.validate_in_xbmc_format(value)

    def _format_option_name(self, option):
        return option.upper()

    def load_preset(
        self, filename, fields_to_apply_to, set_invalid_fields_to_default=True
    ):
        if not os.path.isfile(filename):
            raise ConfigPresetDoesNotExistError(
                "Preset '" + filename + "' does not exist"
            )
        preset_config = self.__class__()
        preset_config.read(
            filename, set_invalid_fields_to_default=set_invalid_fields_to_default
        )

        for field in fields_to_apply_to:
            self.set(field, preset_config.get(field))

    def get(self, option, do_validation=True):
        if do_validation:
            option = self._format_option_name(option)
            self._validate_option_name(option)
        value_in_config_format = self._get_in_config_format(option)
        format_converter = self._format_converters[option]
        return format_converter.convert_to_xbmc_control_format(value_in_config_format)

    def _get_in_config_format(self, option):
        return self._config_parser.get(ConfigParser.DEFAULTSECT, option)

    def set_to_default(self, option):
        option = self._format_option_name(option)
        self.set(option, self._defaults[option])

    def set(self, option, value, do_validation=True):
        if do_validation:
            option = self._format_option_name(option)
            self._validate_option_name_and_value(option, value)
        format_converter = self._format_converters[option]
        value_in_config_format = format_converter.convert_to_config_file_format(value)
        return self._set_in_config_format(option, value_in_config_format)

    def _set_in_config_format(self, option, value):
        return self._config_parser.set(ConfigParser.DEFAULTSECT, option, value)

    def write(self, fp, dont_write_if_default=True):
        stream = StringIO()
        true_if_non_default = self._get_true_if_non_default()
        for field in true_if_non_default:
            value = False
            for field_to_check in true_if_non_default[field]:
                if self.get(field_to_check) != self._defaults[field_to_check]:
                    value = True
                    break
            self.set(field, value)
        true_if_non_zero = self._get_true_if_non_zero()
        for field in true_if_non_zero:
            value = False
            for field_to_check in true_if_non_zero[field]:
                if self.get(field_to_check):
                    value = True
                    break
            self.set(field, value)

        if self._quote_char_if_whitespace:
            for field in self._options:
                value = self._get_in_config_format(field)
                if re.search(r"\s", value):
                    value = (
                        self._quote_char_if_whitespace
                        + value
                        + self._quote_char_if_whitespace
                    )
                    self._set_in_config_format(field, value)

        if dont_write_if_default:
            output_file = ConfigParser.RawConfigParser()
            output_file.optionxform = self._format_option_name
            for field in self._options:
                if (
                    field not in self._defaults
                    or self.get(field) != self._defaults[field]
                ):
                    value_in_config_format = self._get_in_config_format(field)
                    output_file.set(
                        ConfigParser.DEFAULTSECT, field, value_in_config_format
                    )
            output_file.write(stream)
        else:
            self._config_parser.write(stream)

        # Ignore the first line which will be a marker for the default section
        stream.seek(0, 0)
        stream.readline()
        # Replace the first non-commented out instance of " = " with "="
        # (iND-BiOS will only see the first 300 characters of every line)
        equals_white_space_regex = re.compile(r"^([^;]+)\s+=\s+")
        for line in stream:
            fp.write(equals_white_space_regex.sub(r"\1=", line))

        if self._quote_char_if_whitespace:
            self._remove_start_end_quote_chars()
