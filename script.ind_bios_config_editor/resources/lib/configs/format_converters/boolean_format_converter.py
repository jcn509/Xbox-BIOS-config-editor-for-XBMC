from .abstract_format_converter import AbstractFormatConverter


class BooleanFormatConverter(AbstractFormatConverter):
    def convert_to_config_file_format(self, value):
        return str(int(value))

    def convert_to_xbmc_control_format(self, value):
        return bool(int(value))
