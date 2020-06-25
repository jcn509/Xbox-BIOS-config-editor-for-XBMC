"""Converts between a tuple of strings and the index at which a given string is
located in the tuple
"""
try:
    # typing not available on XBMC4XBOX
    from typing import Tuple
except:
    pass

from .abstract_format_converter import AbstractFormatConverter


class DiscreteFormatConverter(AbstractFormatConverter):
    """Converts between a tuple of strings and the index at which a given
    string is located in the tuple
    """

    def __init__(self, values):
        # type: (Tuple[str, ...]) -> None
        self._values = tuple(values)

    def convert_to_config_file_format(self, value):
        """:returns: the index (as a string) at which the value exists in the tuple"""
        # type: (str) -> str
        return str(self._values.index(value))

    def convert_to_python_format(self, index):
        """:returns: the str at the index supplied"""
        # type: (str) -> str
        return self._values[int(index)]
