import re
from .abstract_validator import AbstractValidator, raise_error


class RegexPatternMatchValidator(AbstractValidator):
    __slots__ = "_regex", "_error_message"

    def __init__(
        self, python_regex_pattern, config_regex_pattern=None, error_message=None
    ):
        self._python_regex_pattern = re.compile(python_regex_pattern)
        self._error_message = error_message
        if config_regex_pattern is not None:
            self._config_regex_pattern = re.compile(config_regex_pattern)
        else:
            self._config_regex_pattern = self._python_regex_pattern

    def validate_against_regex(self, value, regex):
        if not isinstance(value, basestring):
            raise_error(
                str(value)
                + " is invalid. Value must be a string that matches pattern "
                + regex.pattern
            )
        if not regex.match(value):
            error_message = self._error_message
            if error_message is None:
                error_message = "must match pattern: " + regex.pattern
            raise_error(value + " is invalid. " + error_message)

    def validate_in_config_file_format(self, value):
        self.validate_against_regex(value, self._config_regex_pattern)

    def validate_in_python_format(self, value):
        self.validate_against_regex(value, self._python_regex_pattern)
