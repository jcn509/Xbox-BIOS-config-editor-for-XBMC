from abc import ABCMeta, abstractmethod
import re

class ConfigField(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, field_name, default):
        self._default = default
        self._field_name = field_name

    # default should be read only
    @property
    def default(self):
        return self._default

    # field_name should be read only
    @property
    def field_name(self):
        return self._field_name

    @abstractmethod
    def validate(self, value):
        pass

class DiscreteField(ConfigField):
    def __init__(self, field_name, default, values):
        self._values = [str(x) for x in values]
        default = str(default)
        super(DiscreteField, self).__init__(field_name, default)
        
    def validate(self, value):
        if value not in self._values:
            raise ValueError(value + " is not valid value for " + self.field_name + " must be one of " + str(self._values))

class BooleanField(DiscreteField):
    def __init__(self, field_name, default):
        super(BooleanField, self).__init__(field_name, default, [0, 1])

class PositionField(DiscreteField):
    def __init__(self, field_name, default):
        super(PositionField, self).__init__(field_name, default, range(-100, 101))

class ZeroToAHundredField(DiscreteField):
    def __init__(self, field_name, default):
        super(ZeroToAHundredField, self).__init__(field_name, default, range(0,101))

class RegexMatchPatternField(ConfigField):
    def __init__(self, field_name, default, regex_pattern, error_message = None):
        self._regex = re.compile(regex_pattern)
        self._error_message = error_message
        if error_message == None:
            self._error_message = field_name + " must match pattern: " + regex_pattern
        super(RegexMatchPatternField, self).__init__(field_name, default)

    def validate(self, value):
        if not self._regex.match(value):
            raise ValueError(value + " is invalid. " + self._error_message)

class HexField(RegexMatchPatternField):
    def __init__(self, field_name, default, length):
        super(HexField, self).__init__(field_name, default, '^0x[0-9a-fA-F]{'+str(length)+'}$')

class ColourField(HexField):
    def __init__(self, field_name, default):
        super(ColourField, self).__init__(field_name, default, 6)

class ColourWithAlphaField(HexField):
    def __init__(self, field_name, default):
        super(ColourWithAlphaField, self).__init__(field_name, default, 8)

class FilePathField(RegexMatchPatternField):
    def __init__(self, field_name, default, device_preabmle, file_extension):
        pattern = "^\\\\Device\\\\" + device_preabmle + "\\\\.+\\." + file_extension + "$"
        super(FilePathField, self).__init__(field_name, default, pattern)

class DvdFilePathField(FilePathField):
    def __init__(self, field_name, default, file_extension):
        super(DvdFilePathField, self).__init__(field_name, default, "CdRom0", file_extension)
        
class DvdXbeFileField(DvdFilePathField):
    def __init__(self, field_name, default):
        super(DvdXbeFileField, self).__init__(field_name, default, "xbe")

class HddFilePathField(FilePathField):
    def __init__(self, field_name, default, file_extension):
        super(HddFilePathField, self).__init__(field_name, default, "Harddisk0\\\\Partition[1267]", file_extension)
        
class HddXbeFileField(HddFilePathField):
    def __init__(self, field_name, default):
        super(HddXbeFileField, self).__init__(field_name, default, "xbe")
        
class HddFilePathOrZeroField(HddFilePathField):
    def validate(self, value):
        if value != '0':
            super(HddFilePathOrZeroField, self).validate(value)
        
class ModelFileField(HddFilePathOrZeroField):
    def __init__(self, field_name, default):
        super(ModelFileField, self).__init__(field_name, default, "x")

