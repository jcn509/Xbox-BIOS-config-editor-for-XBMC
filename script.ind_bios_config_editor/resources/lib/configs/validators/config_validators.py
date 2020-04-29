from abc import ABCMeta, abstractmethod
import re


class AbstractValidator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_in_config_format(self, value):
        raise NotImplementedError

    @abstractmethod
    def validate_in_xbmc_format(self, value):
        raise NotImplementedError


class DiscreteValidator(AbstractValidator):
    __slots__ = "_values"

    def __init__(self, values):
        self._values = [str(x) for x in values]

    def validate_in_config_format(self, value):
        if value not in self._values:
            raise ValueError(value + " is not valid value must be one of " + str(self._values))

    def validate_in_xbmc_format(self, value):
        if value not in self._values:
            raise ValueError(value + " is not valid value must be one of " + str(self._values))

class IntegerValidator(AbstractValidator):
    __slots__ = "_min_value", "_max_value"

    def __init__(self, min_value, max_value):
        self._min_value = min_value
        self._max_value = max_value

    def validate_in_config_format(self, value):
        if value < self._min_value or value > self._max_value:
            raise ValueError(value + " is not valid, value must be >= " + str(self._min_value) + " and <= " + str(self._max_value))

    def validate_in_xbmc_format(self, value):
        self.validate_in_config_format(int(value))


class BooleanValidator(IntegerValidator):
    def __init__(self):
        super(BooleanValidator, self).__init__(0, 1)


class RegexMatchPatternValidator(AbstractValidator):
    __slots__ = "_regex", "_error_message"

    def __init__(self, xbmc_regex_pattern, config_regex_pattern = None, error_message = None):
        self._xbmc_regex_pattern = re.compile(xbmc_regex_pattern)
        self._error_message = error_message
        if config_regex_pattern:
            self._config_regex_pattern = re.compile(config_regex_pattern)
        else:
            self._config_regex_pattern = self._xbmc_regex_pattern

    def validate_against_regex(self, value, regex):
        if not regex.match(value):
            error_message = self._error_message
            if error_message is None:
                error_message = "must match pattern: " + regex.pattern
            raise ValueError(value + " is invalid. " + error_message)

    def validate_in_config_format(self, value):
        self.validate_against_regex(value, self._config_regex_pattern)
    
    def validate_in_xbmc_format(self, value):
        self.validate_against_regex(value, self._xbmc_regex_pattern)

class HexValidator(RegexMatchPatternValidator):
    def __init__(self, length):
        super(HexValidator, self).__init__('^0x[0-9a-fA-F]{' + str(length) + '}$')


class ColourValidator(HexValidator):
    def __init__(self):
        super(ColourValidator, self).__init__(6)


class ColourWithAlphaValidator(HexValidator):
    def __init__(self):
        super(ColourWithAlphaValidator, self).__init__(8)


class FilePathValidator(RegexMatchPatternValidator):
    def __init__(self, device_preabmle, drive_letters_regex, file_extension):
        xbmc_pattern = "^" +drive_letters_regex + ":\\\\.+\\." + file_extension + "$"
        config_pattern = "^\\\\Device\\\\" + device_preabmle + "\\\\.+\\." + file_extension + "$"
        super(FilePathValidator, self).__init__(xbmc_pattern, config_pattern)


class DVDFilePathValidator(FilePathValidator):
    def __init__(self, file_extension):
        super(DVDFilePathValidator, self).__init__( "CdRom0", "D", file_extension)

class HDDFilePathValidator(FilePathValidator):
    def __init__(self, file_extension):
        super(HDDFilePathValidator, self).__init__("Harddisk0\\\\Partition[1267]", "[CEFG]", file_extension)


class OptionalHDDFilePathValidator(HDDFilePathValidator):
    def validate_in_config_format(self, value):
        if value != '0':
            super(OptionalHDDFilePathValidator, self).validate_in_config_format(value)
    
    def validate_in_config_format(self, value):
        if value != None:
            super(OptionalHDDFilePathValidator, self).validate_in_config_format(value)

