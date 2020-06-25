"""Convert integers to strings and vice versa"""
from .abstract_format_converter import AbstractFormatConverter


class IntegerFormatConverter(AbstractFormatConverter):
    """Convert integers to strings and vice versa"""

    def convert_to_config_file_format(self, value):
        """Convert an integer value to a string"""
        # type: (int) -> str
        return str(value)

    def convert_to_python_format(self, value):
        """Convert a string value to an integer"""
        # type: (str) -> int
        return int(value)
