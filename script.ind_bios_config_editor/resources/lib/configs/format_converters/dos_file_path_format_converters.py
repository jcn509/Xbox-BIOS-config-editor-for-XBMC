"""Converts between the path format \Device\<devicename>\partition\... to the
DOS format (C:\...)
"""
try:
    # typing not available on XBMC4XBOX
    from typing import Union
except:
    pass
from .abstract_format_converter import AbstractFormatConverter


class DOSFilePathFormatConverter(AbstractFormatConverter):
    """Converts between the path format \\Device\\<devicename>\\partition\\... to
    the DOS format (C:\\...)
    """

    _DRIVE_PARTITION_MAPPING = {"C": 2, "E": 1, "F": 6, "G": 7}
    _FILE_PATH_PREAMBLE_HDD = "\\Device\\Harddisk0\\Partition"
    _FILE_PATH_PREAMBLE_DVD = "\\Device\\CdRom0"

    def convert_to_config_file_format(self, file_path):
        """Convert from the file path format format C:\\... to \\Device\\..."""
        # type: (str) -> str
        drive_letter = file_path[0]
        if drive_letter in self._DRIVE_PARTITION_MAPPING.keys():
            partition_number = self._DRIVE_PARTITION_MAPPING[drive_letter]
            file_path = (
                self._FILE_PATH_PREAMBLE_HDD + str(partition_number) + file_path[2:]
            )
        elif drive_letter == "D":
            file_path = self._FILE_PATH_PREAMBLE_DVD + file_path[2:]

        return file_path

    def convert_to_python_format(self, file_path):
        """Convert from the file path format format \\Device\\... to C:\\..."""
        # type: (str) -> str
        if file_path.startswith(self._FILE_PATH_PREAMBLE_HDD):
            file_path = file_path.replace(self._FILE_PATH_PREAMBLE_HDD, "")
            partition_number = int(file_path[0])
            drive_letter = None
            for letter in self._DRIVE_PARTITION_MAPPING:
                if self._DRIVE_PARTITION_MAPPING[letter] == partition_number:
                    drive_letter = letter
                    break
            file_path = drive_letter + ":" + file_path[1:]
        elif file_path.startswith(self._FILE_PATH_PREAMBLE_DVD):
            file_path = "D:" + file_path.replace(self._FILE_PATH_PREAMBLE_DVD, "")

        return file_path


class OptionalDOSFilePathFormatConverter(DOSFilePathFormatConverter):
    """Converts between the path format \\Device\\<devicename>\\partition\\... to
    the DOS format (C:\\...). Also allows for values that specify no file.
    """

    def convert_to_config_file_format(self, file_path):
        """Convert from the file path format format C:\\... to \\Device\\...

        Also convert None to the string 0
        """
        # type: (Union[str, None]) -> str

        if file_path == None:
            return "0"
        return super(
            OptionalDOSFilePathFormatConverter, self
        ).convert_to_config_file_format(file_path)

    def convert_to_python_format(self, file_path):
        """Convert from the file path format format \\Device\\... to C:\\...
        
        Also convert the string 0 to None
        """
        # type: (str) -> Union[str, None]

        if file_path == "0":
            return None
        return super(OptionalDOSFilePathFormatConverter, self).convert_to_python_format(
            file_path
        )
