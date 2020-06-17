from .abstract_validator import AbstractValidator, raise_error


class DiscreteValidator(AbstractValidator):
    __slots__ = "_values"

    def __init__(self, python_format_values, config_format_values=None):
        self._python_format_values = [str(x) for x in python_format_values]
        if config_format_values is None:
            config_format_values = [str(x) for x in range(len(python_format_values))]
        self._config_format_values = config_format_values

    def validate_in_config_file_format(self, value):
        if value not in self._config_format_values:
            raise_error(
                value
                + " is not valid value must be one of "
                + str(self._config_format_values)
            )

    def validate_in_python_format(self, value):
        if value not in self._python_format_values:
            raise_error(
                value
                + " is not valid value must be one of "
                + str(self._python_format_values)
            )
