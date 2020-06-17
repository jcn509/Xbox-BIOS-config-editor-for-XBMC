from .abstract_format_converter import AbstractFormatConverter

# Doesn't actually need to do anything...
class StringFormatConverter(AbstractFormatConverter):
    def convert_to_config_file_format(self, value):
        return value

    def convert_to_python_format(self, value):
        return value
