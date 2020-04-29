import ConfigParser
from StringIO import StringIO
import os
import re
from abc import ABCMeta, abstractmethod
from .config_errors import ConfigError, ConfigFieldNameError, ConfigFieldValueError, ConfigPresetDoesNotExistError
from .validators import validator_factory
from .format_converters import format_converter_factory

_DEFAULT_SECTION = "DEFAULT"

class AbstractConfig(ConfigParser.RawConfigParser, object):
    __metaclass__ = ABCMeta

    def __init__(self, max_line_length=None, quote_char_if_whitespace=None, *args, **kwargs):
        fields = self._get_fields()
        self._options = tuple(field.field_name for field in fields)

        defaults = {field.field_name: field.default_value for field in fields}
        self._format_converters = {field.field_name: format_converter_factory(field) for field in fields}
        self._validators = {field.field_name: validator_factory(field) for field in fields}

        self._max_line_length = max_line_length
        self._quote_char_if_whitespace = quote_char_if_whitespace
 
        super(AbstractConfig, self).__init__(*args, **kwargs)
        self._defaults = defaults

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

    def read(self, filenames, set_invalid_fields_to_default=True, *args, **kwargs):
        if isinstance(filenames, basestring):
            filenames = [filenames]

        read_ok = []
        for filename in filenames:
            try:
                with open(filename) as fp:
                    self.readfp(fp, set_invalid_fields_to_default=set_invalid_fields_to_default, *args, **kwargs)
            except IOError:
                continue
            else:
                read_ok.append(filename)

        return read_ok

    def _remove_start_end_quote_chars(self):
        if self._quote_char_if_whitespace:
            for field in self._options:
                value = self.get(field, do_validation=False)
                if value[0] == self._quote_char_if_whitespace and value[-1] == self._quote_char_if_whitespace:
                    self.set(field, value[1:-1], do_validation=False)


    def readfp(self, fp, set_invalid_fields_to_default=True, *args, **kwargs):
        stream = StringIO()

        try:
            stream.name = fp.name
        except AttributeError:
            pass

        stream.write('[' + _DEFAULT_SECTION + ']\n')
        stream.write(fp.read())
        stream.seek(0, 0)

        super(AbstractConfig, self).readfp(stream, *args, **kwargs)
        if self._quote_char_if_whitespace:
            self._remove_start_end_quote_chars()
        self._validate_everything(set_invalid_fields_to_default)

    def _validate_everything_in_config_format(self, set_invalid_fields_to_default=False):
        for option in self.options():
            value = self._get_in_config_format(option)
            if set_invalid_fields_to_default:
                try:
                    self._validate_option_name_and_value(option, value, value_in_config_format = True)
                except ConfigError:
                    self.set_to_default(option)
            else:
                self._validate_option_name_and_value(option, value, value_in_config_format = True)

    def _validate_option_name(self, option_name):
        if option_name not in self._options:
            raise ConfigFieldNameError(option_name + " is not a valid option")

    def _validate_option_name_and_value(self, option_name, value, value_in_config_format = False):
        self._validate_option_name(option_name)

        # Won't reach this if option name is invalid
        # (which is what we want as there will be no validator
        # if the option does not exist)
        validator = self._validators[option_name]
        if value_in_config_format:
            validator.validate_in_config_format(value)
            if self._max_line_length and self._quote_char_if_whitespace is not None:
                # The equals sign, the 2 spaces around it and \r\n on the end of line
                additional_chars = 5
                if re.search(r"\s", value):
                    # The quotes around the value
                    additional_chars += 2 * len(self._quote_char_if_whitespace)
                if len(option_name) + len(value) + additional_chars > self._max_line_length:
                    raise ConfigFieldValueError("Cannot use " + value + " for field " + option_name +
                                    " the line length in the file would be too long")
        else:
            validator.validate_in_xbmc_format(value)

    def optionxform(self, option):
        return option.upper()

    def load_preset(self, filename, fields_to_apply_to, set_invalid_fields_to_default=True):
        if not os.path.isfile(filename):
            raise ConfigPresetDoesNotExistError("Preset '" + filename + "' does not exist")
        preset_config = self.__class__()
        preset_config.read(filename, set_invalid_fields_to_default=set_invalid_fields_to_default)

        for field in fields_to_apply_to:
            self.set(field, preset_config.get(field))

    def get(self, option, do_validation=True):
        if do_validation:
            option = self.optionxform(option)
            self._validate_option_name(option)
        value_in_config_format = super(AbstractConfig, self).get(_DEFAULT_SECTION, option)
        format_converter = self._format_converters[option]
        return format_converter.convert_to_xbmc_control_format(value_in_config_format)

    def _get_in_config_format(self, option):
        return super(AbstractConfig, self).get(_DEFAULT_SECTION, option)

    def items(self):
        return super(AbstractConfig, self).items(_DEFAULT_SECTION)

    def set_to_default(self, option):
        option = self.optionxform(option)
        self.set(option, self.defaults()[option])

    def set(self, option, value, do_validation=True):
        if do_validation:
            option = self.optionxform(option)
            self._validate_option_name_and_value(option, value)
        format_converter = self._format_converters[option]
        value_in_config_format = format_converter.convert_to_config_file_format(value)
        return super(AbstractConfig, self).set(_DEFAULT_SECTION, option, value_in_config_format)

    def write(self, fp, dont_write_if_default=True):
        stream = StringIO()
        defaults_dict = self.defaults()
        true_if_non_default = self._get_true_if_non_default()
        for field in true_if_non_default:
            value = False
            for field_to_check in true_if_non_default[field]:
                if self.get(field_to_check) != defaults_dict[field_to_check]:
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
                value = self.get(field, do_validation=False)
                if re.search(r"\s", value):
                    value = self._quote_char_if_whitespace + value + self._quote_char_if_whitespace
                    self.set(field, value)

        if dont_write_if_default:
            output_file = ConfigParser.RawConfigParser()
            output_file.add_section(_DEFAULT_SECTION)
            output_file.optionxform = self.optionxform
            for field in self._options:
                value = self.get(field, do_validation=False)
                if field not in defaults_dict or \
                        value != defaults_dict[field]:
                    output_file.set(_DEFAULT_SECTION, field, value)
            output_file.write(stream)
        else:
            super(AbstractConfig, self).write(stream)

        # Ignore the first line which will be the marker for the default section
        stream.seek(0, 0)
        stream.readline()
        fp.write(stream.read())

        if self._quote_char_if_whitespace:
            self._remove_start_end_quote_chars()
