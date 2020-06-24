"""Validate integer values. They should be strings in config file format"""
from .abstract_validator import AbstractValidator
from ..config_errors import ConfigFieldValueError

class IntegerValidator(AbstractValidator):
    """Validate integer values. They should be strings in config file format"""
    __slots__ = "_min_value", "_max_value"

    def __init__(self, min_value, max_value):
        # type: (int, int) -> None
        self._min_value = min_value
        self._max_value = max_value

    def validate_in_config_file_format(self, value):
        """:raises ConfigFieldValueError: if value is not a string consisting\
                only of numbers such that min_value <= value <= max_value
        """
        if not isinstance(value, basestring):
            raise ConfigFieldValueError("Value must be a string not " + str(type(value)))
        if not value.lstrip('-').isdigit():
            raise ConfigFieldValueError(value + " contains characters that are not digits or -")
        self.validate_in_python_format(int(value))

    def validate_in_python_format(self, value):
        """:raises ConfigFieldValueError: if value is not an int or long such\
                thatmin_value <= value <= max_value
        """
        if not isinstance(value, (int, long)):
            raise ConfigFieldValueError("Value must be an int or long not " + str(type(value)))
        if value < self._min_value or value > self._max_value:
            raise ConfigFieldValueError(
                str(value)
                + " is not valid, value must be >= "
                + str(self._min_value)
                + " and <= "
                + str(self._max_value)
            )
