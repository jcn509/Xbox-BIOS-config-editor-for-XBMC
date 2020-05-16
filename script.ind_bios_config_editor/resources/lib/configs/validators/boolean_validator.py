from .abstract_validator import AbstractValidator, raise_error


class BooleanValidator(AbstractValidator):
    def validate_in_config_format(self, value):
        if value not in ("0", "1"):
            raise_error(str(value) + " is not valid, value must be 0 or 1")

    def validate_in_python_format(self, value):
        # Need to check type to stop accepting 1 or 0
        if value not in (True, False) or not isinstance(value, bool):
            raise_error(str(value) + " is not valid, value must be True or False")
