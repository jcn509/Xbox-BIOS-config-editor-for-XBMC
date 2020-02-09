from .abstract_converter import AbstractConverter


class Enum(AbstractConverter):

    def __init__(self, enum_type):
        self._enum_values = tuple(enum_type)

    def convert_to_config_file_format(self, value):
        return self._enum_values.index(value)

    def convert_to_xbmc_control_format(self, value):
        return self._enum_values[int(value)]
