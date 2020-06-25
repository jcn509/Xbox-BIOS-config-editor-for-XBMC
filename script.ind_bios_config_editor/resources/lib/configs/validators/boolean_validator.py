"""Validate boolean values.
Booleans in config format are represented by the strings 0 and 1
"""
from .abstract_validator import AbstractValidator
from ..config_errors import ConfigFieldValueError


class BooleanValidator(AbstractValidator):
    """Validate boolean values.
    Booleans in config format are represented by the strings 0 and 1
    """

    def validate_in_config_file_format(self, value):
        """:raises ConfigFieldValueError: if value is not the string 0 or the string 1"""
        if value not in ("0", "1"):
            raise ConfigFieldValueError(
                str(value) + " is not valid, value must be 0 or 1"
            )

    def validate_in_python_format(self, value):
        """:raises ConfigFieldValueError: if value is not True or False"""
        # Need to check type to stop accepting 1 or 0
        if value not in (True, False) or not isinstance(value, bool):
            raise ConfigFieldValueError(
                str(value) + " is not valid, value must be True or False"
            )
