from abc import ABCMeta, abstractmethod
import re


class AbstractValidator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate(self, value):
        raise NotImplementedError


class DiscreteField(AbstractValidator):
    __slots__ = "_values"

    def __init__(self, values):
        self._values = [str(x) for x in values]

    def validate(self, value):
        if value not in self._values:
            raise ValueError(value + " is not valid value must be one of " + str(self._values))


class BooleanField(DiscreteField):
    def __init__(self):
        super(BooleanField, self).__init__((0, 1))


class PositionField(DiscreteField):
    def __init__(self):
        super(PositionField, self).__init__(range(-100, 101))


class ZeroToAHundredField(DiscreteField):
    def __init__(self):
        super(ZeroToAHundredField, self).__init__(range(0, 101))


class RegexMatchPatternField(AbstractValidator):
    __slots__ = "_regex", "_error_message"

    def __init__(self, regex_pattern, error_message = None):
        self._regex = re.compile(regex_pattern)
        self._error_message = error_message
        if error_message is None:
            self._error_message = "must match pattern: " + regex_pattern

    def validate(self, value):
        if not self._regex.match(value):
            raise ValueError(value + " is invalid. " + self._error_message)


class HexField(RegexMatchPatternField):
    def __init__(self, length):
        super(HexField, self).__init__('^0x[0-9a-fA-F]{' + str(length) + '}$')


class ColourField(HexField):
    def __init__(self):
        super(ColourField, self).__init__(6)


class ColourWithAlphaField(HexField):
    def __init__(self):
        super(ColourWithAlphaField, self).__init__(8)


class FilePathField(RegexMatchPatternField):
    def __init__(self, device_preabmle, file_extension):
        pattern = "^\\\\Device\\\\" + device_preabmle + "\\\\.+\\." + file_extension + "$"
        super(FilePathField, self).__init__(pattern)


class DvdFilePathField(FilePathField):
    def __init__(self, file_extension):
        super(DvdFilePathField, self).__init__( "CdRom0", file_extension)


class DvdXbeFileField(DvdFilePathField):
    def __init__(self):
        super(DvdXbeFileField, self).__init__("xbe")


class HddFilePathField(FilePathField):
    def __init__(self, file_extension):
        super(HddFilePathField, self).__init__("Harddisk0\\\\Partition[1267]", file_extension)


class HddXbeFileField(HddFilePathField):
    def __init__(self):
        super(HddXbeFileField, self).__init__("xbe")


class HddFilePathOrZeroField(HddFilePathField):
    def validate(self, value):
        if value != '0':
            super(HddFilePathOrZeroField, self).validate(value)


class ModelFileField(HddFilePathOrZeroField):
    def __init__(self):
        super(ModelFileField, self).__init__("x")
