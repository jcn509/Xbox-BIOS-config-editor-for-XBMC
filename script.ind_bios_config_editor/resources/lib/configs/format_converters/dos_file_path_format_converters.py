from .abstract_format_converter import AbstractFormatConverter


class DOSFilePathFormatConverter(AbstractFormatConverter):
    _DRIVE_PARTITION_MAPPING = {"C": 2, "E": 1, "F": 6, "G": 7}
    _FILE_PATH_PREAMBLE_HDD = "\\Device\\Harddisk0\\Partition"
    _FILE_PATH_PREAMBLE_DVD = "\\Device\\CdRom0"

    def convert_to_config_file_format(self, value):
        drive_letter = value[0]
        if drive_letter in self._DRIVE_PARTITION_MAPPING.keys():
            partition_number = self._DRIVE_PARTITION_MAPPING[drive_letter]
            value = self._FILE_PATH_PREAMBLE_HDD + str(partition_number) + value[2:]
        elif drive_letter == "D":
            value = self._FILE_PATH_PREAMBLE_DVD + value[2:]

        return value

    def convert_to_python_format(self, value):
        if value.startswith(self._FILE_PATH_PREAMBLE_HDD):
            value = value.replace(self._FILE_PATH_PREAMBLE_HDD, "")
            partition_number = int(value[0])
            drive_letter = None
            for letter in self._DRIVE_PARTITION_MAPPING:
                if self._DRIVE_PARTITION_MAPPING[letter] == partition_number:
                    drive_letter = letter
                    break
            value = drive_letter + ":" + value[1:]
        elif value.startswith(self._FILE_PATH_PREAMBLE_DVD):
            value = "D:" + value.replace(self._FILE_PATH_PREAMBLE_DVD, "")

        return value


class OptionalDOSFilePathFormatConverter(DOSFilePathFormatConverter):
    def convert_to_config_file_format(self, value):
        if value == None:
            return "0"
        return super(
            OptionalDOSFilePathFormatConverter, self
        ).convert_to_config_file_format(value)

    def convert_to_python_format(self, value):
        if value == "0":
            return None
        return super(OptionalDOSFilePathFormatConverter, self).convert_to_python_format(
            value
        )