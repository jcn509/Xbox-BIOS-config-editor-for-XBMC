from .. import controls
from .abstract_converter import AbstractConverter


class IndBios(AbstractConverter):
    _DRIVE_PARTITION_MAPPING = {
        "C": 2,
        "E": 1,
        "F": 6,
        "G": 7
    }
    _FILE_PATH_PREAMBLE = "\\Device\\Harddisk0\\Partition"

    def _convert_file_path_to_config_format(self, value):
        drive_letter = value[0]
        if drive_letter in ["C", "E", "F", "G"]:
            drive_letter = value[0]
            partition_number = self._DRIVE_PARTITION_MAPPING[drive_letter]
            value = self._FILE_PATH_PREAMBLE + str(partition_number) + value[2:]
        # elif drive_letter == "D":
        # value = "\\Device\\Harddisk0\\Partition" + partition_number[drive_letter] + value[2:]
        else:
            raise ValueError("Cannot select file from drive " + drive_letter)

        return value

    def convert_to_config_format(self, section, field, value, control):
        control_type = type(control)

        if section in self._control_to_config and field in self._control_to_config[section]:
            value = self._control_to_config[section][field](value)
        elif control_type == controls.RadioButton:
            value = self._convert_boolean_to_config_format(value)
        elif control_type == controls.FileSelector:
            value = self._convert_file_path_to_config_format(value)
        else:
            value = str(value)

        return value

    def _convert_file_path_to_control_format(self, value):
        value = value.replace(self._FILE_PATH_PREAMBLE, "")
        partition_number = int(value[0])
        drive_letter = None
        for letter in self._DRIVE_PARTITION_MAPPING:
            if self._DRIVE_PARTITION_MAPPING[letter] == partition_number:
                drive_letter = letter
                break
        if drive_letter == None:
            raise ValueError("Error converting \"" + value + "\" to a DOS style file path")
        value = drive_letter + ":" + value[1:]

        return value

    def _convert_integer_value_to_control_format(self, value):
        return int(value)

    def convert_to_control_format(self, section, field, value, control):
        control_type = type(control)

        if section in self._config_to_control and field in self._config_to_control[section]:
            value = self._config_to_control[section][field](value)
        elif control_type == controls.RadioButton:
            value = self._convert_boolean_to_control_format(value)
        elif control_type == controls.FileSelector:
            value = self._convert_file_path_to_control_format(value)
        elif control_type == controls.FakeSlider:
            value = int(value)

        return value
