from .abstract_converter import AbstractConverter


class Integer(AbstractConverter):

    def convert_to_config_file_format(self, value):
        return str(value)

    def convert_to_xbmc_control_format(self, value):
        return int(value)
