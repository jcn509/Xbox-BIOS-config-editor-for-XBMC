"""Kind of a dummy format converter. Does nothing to its inputs"""
from .abstract_format_converter import AbstractFormatConverter

# Doesn't actually need to do anything...
class StringFormatConverter(AbstractFormatConverter):
    """Kind of a dummy format converter. Does nothing to its inputs"""
    def convert_to_config_file_format(self, value):
        """Returns its input"""
        # type: (str) -> str
        return value

    def convert_to_python_format(self, value):
        """Returns its input"""
        # type: (str) -> str
        return value
