"""Validate file paths"""
import re
from ..config_errors import ConfigFieldValueError
from .regex_pattern_match_validator import RegexPatternMatchValidator


class _FilePathValidator(RegexPatternMatchValidator):
    """Helper class used for any file path whether it is DVD or HDD"""
    def __init__(self, device_preabmle, drive_letters_regex, file_extension):
        # type: (str, str, str) -> None
        xbmc_pattern = "^" + drive_letters_regex + ":\\\\.+\\." + file_extension + "$"
        config_pattern = (
            "^\\\\Device\\\\" + device_preabmle + "\\\\.+\\." + file_extension + "$"
        )
        super(_FilePathValidator, self).__init__(xbmc_pattern, config_pattern)


class DVDFilePathValidator(_FilePathValidator):
    """Validator for files on a DVD
    
    config file format values must start with \\Device\\CdRom0\\
    Python format values must start with D:\\
    """
    def __init__(self, file_extension):
        super(DVDFilePathValidator, self).__init__("CdRom0", "D", file_extension)


class HDDFilePathValidator(_FilePathValidator):
    """Validator for files on the HDD
    
    config file format values must start with
    \\Device\\Harddisk0\\Partition{1, 2, 6, 7}
    Python format values must start with {C, E, F, G}:\\

    This means that files cannot be on the cache partitions (X, Y, Z)
    """
    def __init__(self, file_extension):
        # type: (str) ->  None
        super(HDDFilePathValidator, self).__init__(
            "Harddisk0\\\\Partition[1267]", "[CEFG]", file_extension
        )


class OptionalHDDFilePathValidator(HDDFilePathValidator):
    """Validator for optional files on the HDD
    
    config file format values must start with
    \\Device\\Harddisk0\\Partition{1, 2, 6, 7} or be the string 0
    Python format values must start with {C, E, F, G}:\\ or be None

    This means that files cannot be on the cache partitions (X, Y, Z)
    """
    def validate_in_config_file_format(self, file_path):
        """:raises ConfigFieldValueError: if file_path is not the string 0 or\
                if it does not start with \
                \\Device\\Harddisk0\\Partition{1, 2, 6, 7} 
        """
        # type: (str) -> None
        if file_path != "0":
            super(OptionalHDDFilePathValidator, self).validate_in_config_file_format(
                file_path
            )

    def validate_in_python_format(self, file_path):
        """:raises ConfigFieldValueError: if file_path is not None or does\
                not start with {C, E, F, G}:\\
        """
        # type: (str) -> None
        if file_path is not None:
            super(OptionalHDDFilePathValidator, self).validate_in_python_format(file_path)
