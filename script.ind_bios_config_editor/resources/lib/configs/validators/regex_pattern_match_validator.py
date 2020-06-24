"""Validator that ensures that values in Python and config file format match
regular expressions (may have one regular expression for the Python format and
a different one for the config file format)
"""
import re
try:
    # typing not available on XBMC4XBOX
    from typing import Pattern
except:
    pass

from .abstract_validator import AbstractValidator
from ..config_errors import ConfigFieldValueError

class RegexPatternMatchValidator(AbstractValidator):
    """Validator that ensures that values in Python and config file format
    match regular expressions

    If config_regex_pattern is not supplied then both Python and config file
    format values will be validated against python_regex_pattern
    """   
    __slots__ = "_regex", "_error_message"

    def __init__(
        self, python_regex_pattern, config_regex_pattern=None, error_message=None
    ):
        """If config_regex_pattern is not supplied then both Python and config
        file format values will be validated against python_regex_pattern
        """
        # type (str, str, str) -> None
        self._python_regex_pattern = re.compile(python_regex_pattern)
        self._error_message = error_message
        if config_regex_pattern is not None:
            self._config_regex_pattern = re.compile(config_regex_pattern)
        else:
            self._config_regex_pattern = self._python_regex_pattern

    def _validate_against_regex(self, value, regex):
        """:raises ConfigFieldValueError: if value is not a string or does\
                not match regex
        """
        # type: (str, Pattern) -> None
        if not isinstance(value, basestring):
            raise ConfigFieldValueError(
                str(value)
                + " is invalid. Value must be a string that matches pattern "
                + regex.pattern
            )
        if not regex.match(value):
            error_message = self._error_message
            if error_message is None:
                error_message = "must match pattern: " + regex.pattern
            raise ConfigFieldValueError(value + " is invalid. " + error_message)

    def validate_in_config_file_format(self, value):
        """:raises ConfigFieldValueError: if value is not a string or does\
                not match config_regex_pattern if that was suppplied or\
                python_regex_pattern ifit was not
        """
        self._validate_against_regex(value, self._config_regex_pattern)

    def validate_in_python_format(self, value):
        """:raises ConfigFieldValueError: if value is not a string or does\
                not match python_regex_pattern
        """
        self._validate_against_regex(value, self._python_regex_pattern)
