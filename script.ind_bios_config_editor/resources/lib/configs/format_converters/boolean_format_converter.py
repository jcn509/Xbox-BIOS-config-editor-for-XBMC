from .abstract_format_converter import AbstractFormatConverter


class BooleanFormatConverter(AbstractFormatConverter):
    def convert_to_config_file_format(self, value):
        return "0" if value == False else "1"

    def convert_to_python_format(self, value):
        return False if value == "0" else True
