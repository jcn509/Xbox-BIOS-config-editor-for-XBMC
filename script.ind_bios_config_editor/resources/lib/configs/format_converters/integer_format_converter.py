from .abstract_format_converter import AbstractFormatConverter


class IntegerFormatConverter(AbstractFormatConverter):
    def convert_to_config_file_format(self, value):
        return str(value)

    def convert_to_python_format(self, value):
        return int(value)
