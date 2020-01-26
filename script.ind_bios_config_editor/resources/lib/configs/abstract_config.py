import ConfigParser
import os
import re
from abc import ABCMeta, abstractmethod


class AbstractConfig(ConfigParser.RawConfigParser, object):
    __metaclass__ = ABCMeta

    def __init__(self, max_line_length=None, quote_char_if_whitespace=None, *args, **kwargs):
        fields = self._get_fields()
        self._field_validators = {section: {field.field_name: field for field in fields[section]} for section in fields}
        defaults_dict = self.defaults()

        self._max_line_length = max_line_length
        self._quote_char_if_whitespace = quote_char_if_whitespace

        super(AbstractConfig, self).__init__(*args, **kwargs)

        for section in defaults_dict:
            self.add_section(section)
            for field in defaults_dict[section]:
                self.set(section, field, defaults_dict[section][field])

    def get_default_section(self):
        return "CONFIG"

    def defaults(self):
        return {section: {key: self._field_validators[section][key].default for key in self._field_validators[section]}
                for
                section in self._field_validators}

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
            for section in self.sections():
                for field in self.options(section):
                    value = self.get(section, field, do_validation=False)
                    if value[0] == self._quote_char_if_whitespace and value[-1] == self._quote_char_if_whitespace:
                        self.set(section, field, value[1:-1], do_validation=False)

    def readfp(self, fp, set_invalid_fields_to_default=True, *args, **kwargs):
        super(AbstractConfig, self).readfp(fp, *args, **kwargs)
        if self._quote_char_if_whitespace:
            self._remove_start_end_quote_chars()
        self._validate_everything(set_invalid_fields_to_default)

    def _validate_everything(self, set_invalid_fields_to_default=False):
        defaults_dict = self.defaults()
        valid_sections = defaults_dict.keys()
        for section in self.sections():
            if section in valid_sections:
                valid_options = defaults_dict[section].keys()
                for option in self.items(section):
                    name = option[0]
                    if name in valid_options:
                        value = option[1]
                        if set_invalid_fields_to_default:
                            try:
                                self._validate_option_name_and_value(section, name, value)
                            except:
                                self.set_to_default(section, name)
                        else:
                            self._validate_option_name_and_value(section, name, value)
            else:
                raise ValueError(section + " is not a valid section")

    def _validate_option_name(self, section, option_name):
        if not self.has_section(section):
            raise ConfigParser.NoSectionError(section + " is not a valid section")
        elif option_name not in self._field_validators[section]:
            raise ValueError(option_name + " is not a valid option in section " + section)

    def _validate_option_name_and_value(self, section, option_name, value):
        self._validate_option_name(section, option_name)

        # Won't reach this if option name is invalid
        # (which is what we want as there will be no validator
        # if the option does not exist)
        self._field_validators[section][option_name].validate(value)
        if self._max_line_length and self._quote_char_if_whitespace is not None:
            # The equals sign, the 2 spaces around it and \r\n on the end of line
            additional_chars = 5
            if re.search(r"\s", value):
                # The quotes around the value
                additional_chars += 2 * len(self._quote_char_if_whitespace)
            if len(option_name) + len(value) + additional_chars > self._max_line_length:
                raise ValueError("Cannot use " + value + " for field " + option_name +
                                 " the line length in the file would be too long")

    def optionxform(self, option):
        return option.upper()

    def load_preset(self, filename, fields_to_apply_to, set_invalid_fields_to_default=True):
        if not os.path.isfile(filename):
            raise ValueError("Preset '" + filename + "' does not exist")
        # Subclasses may do extra processing etc
        # and will have the validators properly defined
        preset_config = self.__class__()
        preset_config.read(filename, set_invalid_fields_to_default=set_invalid_fields_to_default)

        for section in fields_to_apply_to:
            for field in fields_to_apply_to[section]:
                self.set(section, field, preset_config.get(section, field))

    def get(self, section, option, do_validation=True):
        if do_validation:
            option = self.optionxform(option)
            self._validate_option_name(section, option)
        return super(AbstractConfig, self).get(section, option)

    def set_to_default(self, section, option):
        option = self.optionxform(option)
        self.set(section, option, self.defaults()[section][option])

    def set(self, section, option, value, do_validation=True):
        if do_validation:
            option = self.optionxform(option)
            self._validate_option_name_and_value(section, option, value)
        return super(AbstractConfig, self).set(section, option, value)

    def write(self, fp, dont_write_if_default=True):
        defaults_dict = self.defaults()
        true_if_non_default = self._get_true_if_non_default()
        for section in true_if_non_default:
            for field in true_if_non_default[section]:
                value = '0'
                for field_to_check in true_if_non_default[section][field]:
                    if self.get(section, field_to_check) != defaults_dict[section][field_to_check]:
                        value = '1'
                        break
                self.set(section, field, value)
        true_if_non_zero = self._get_true_if_non_zero()
        for section in true_if_non_zero:
            for field in true_if_non_zero[section]:
                value = '0'
                for field_to_check in true_if_non_zero[section][field]:
                    if self.get(section, field_to_check) != '0':
                        value = '1'
                        break
                self.set(section, field, value)

        if self._quote_char_if_whitespace:
            for section in self.sections():
                for field in self.options(section):
                    value = self.get(section, field, do_validation=False)
                    if re.search(r"\s", value):
                        value = self._quote_char_if_whitespace + value + self._quote_char_if_whitespace
                        self.set(section, field, value)

        if dont_write_if_default:
            output_file = ConfigParser.RawConfigParser()
            output_file.optionxform = self.optionxform
            for section in self.sections():
                for field in self.options(section):
                    value = self.get(section, field, do_validation=False)
                    if section not in defaults_dict or field not in defaults_dict[section] or \
                            value != defaults_dict[section][field]:
                        if not output_file.has_section(section):
                            output_file.add_section(section)
                        output_file.set(section, field, value)
            output_file.write(fp)
        else:
            super(AbstractConfig, self).write(fp)

        if self._quote_char_if_whitespace:
            self._remove_start_end_quote_chars()
