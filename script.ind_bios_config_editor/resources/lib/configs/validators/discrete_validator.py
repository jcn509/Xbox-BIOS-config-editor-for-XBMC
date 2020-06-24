"""Validate values that should be:
 - In Python format: one string from a tuple of strings
 - In config file format either:
  - one string from a tuple of strings or if this tuple is supplied
  - an index (as a string) of a string from the Python format strings tuple
"""
try:
    # typing not available on XBMC4XBOX
    from typing import Tuple
except:
    pass
from .abstract_validator import AbstractValidator
from ..config_errors import ConfigFieldValueError

class DiscreteValidator(AbstractValidator):
    """Validate values that should be:
     - In Python format: one string from a tuple of strings
     - In config file format either:
      - one string from a tuple of strings or if this tuple is supplied
      - an index (as a string) of a string from the Python format strings tuple
    """

    __slots__ = "_values"

    def __init__(self, python_format_values, config_format_values=None):
        """if config_format_values is not supplied then config file format
        values will be validated against python_format_values
        """
        # type: (Tuple[str, ...], Tuple[str, ...]) -> None
        self._python_format_values = [str(x) for x in python_format_values]
        if config_format_values is None:
            config_format_values = [str(x) for x in range(len(python_format_values))]
        self._config_format_values = config_format_values

    def validate_in_config_file_format(self, value):
        """:raises ConfigFieldValueError: if value is not in\
                config_format_values if that was supplied or an index (as a\
                string) of a value in python_format_values if it was not
        """
        if value not in self._config_format_values:
            raise ConfigFieldValueError(
                value
                + " is not valid value must be one of "
                + str(self._config_format_values)
            )

    def validate_in_python_format(self, value):
        """:raises ConfigFieldValueError: if value is not in python_format_values"""
        if value not in self._python_format_values:
            raise ConfigFieldValueError(
                value
                + " is not valid value must be one of "
                + str(self._python_format_values)
            )
