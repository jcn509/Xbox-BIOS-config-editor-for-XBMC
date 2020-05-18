import re
from .regex_pattern_match_validator import RegexPatternMatchValidator


class FilePathValidator(RegexPatternMatchValidator):
    def __init__(self, device_preabmle, drive_letters_regex, file_extension):
        xbmc_pattern = "^" + drive_letters_regex + ":\\\\.+\\." + file_extension + "$"
        config_pattern = (
            "^\\\\Device\\\\" + device_preabmle + "\\\\.+\\." + file_extension + "$"
        )
        super(FilePathValidator, self).__init__(xbmc_pattern, config_pattern)


class DVDFilePathValidator(FilePathValidator):
    def __init__(self, file_extension):
        super(DVDFilePathValidator, self).__init__("CdRom0", "D", file_extension)


class HDDFilePathValidator(FilePathValidator):
    def __init__(self, file_extension):
        super(HDDFilePathValidator, self).__init__(
            "Harddisk0\\\\Partition[1267]", "[CEFG]", file_extension
        )


class OptionalHDDFilePathValidator(HDDFilePathValidator):
    def validate_in_config_format(self, value):
        if value != "0":
            super(OptionalHDDFilePathValidator, self).validate_in_config_format(value)

    def validate_in_python_format(self, value):
        if value is not None:
            super(OptionalHDDFilePathValidator, self).validate_in_python_format(value)
