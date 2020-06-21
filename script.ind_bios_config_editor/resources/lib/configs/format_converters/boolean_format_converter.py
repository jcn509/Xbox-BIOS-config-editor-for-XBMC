"""Converts boolean values between their bool and str representation"""
from .abstract_format_converter import AbstractFormatConverter


class BooleanFormatConverter(AbstractFormatConverter):
    """Converts boolean values between their bool and str representation"""
    def convert_to_config_file_format(self, value):
        """Convert a boolean to the string 1 or 0"""
        # type: (bool) -> str
        return "0" if value == False else "1"

    def convert_to_python_format(self, value):
        """Convert the string 1 or 0 to boolean True or False"""
        # type: (str) -> bool
        return False if value == "0" else True
