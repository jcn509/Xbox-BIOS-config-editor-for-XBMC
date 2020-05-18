from .abstract_validator import AbstractValidator, raise_error


class IntegerValidator(AbstractValidator):
    __slots__ = "_min_value", "_max_value"

    def __init__(self, min_value, max_value):
        self._min_value = min_value
        self._max_value = max_value

    def validate_in_config_format(self, value):
        self.validate_in_python_format(int(value))

    def validate_in_python_format(self, value):
        if not isinstance(value, (int, long)):
            raise_error("Value must be an int or long not " + str(type(value)))
        if value < self._min_value or value > self._max_value:
            raise_error(
                str(value)
                + " is not valid, value must be >= "
                + str(self._min_value)
                + " and <= "
                + str(self._max_value)
            )
