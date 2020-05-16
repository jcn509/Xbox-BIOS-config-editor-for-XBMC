import pytest
from resources.lib.configs import ConfigFieldValueError
from resources.lib.configs.validators import BooleanValidator

_BOOLEAN_VALIDATOR = BooleanValidator()

@pytest.mark.parametrize(
    "value",
    (True, False)
)
def test_validate_in_python_format_valid(value):
    # No error thrown
    _BOOLEAN_VALIDATOR.validate_in_python_format(value)

@pytest.mark.parametrize(
    "value",
    (1, 0, "1", "0", "True", "False", "", [], [True])
)
def test_validate_in_python_format_invalid(value):
    check error message
    with pytest.raises(ConfigFieldValueError):
        _BOOLEAN_VALIDATOR.validate_in_python_format(value)

@pytest.mark.parametrize(
    "value",
    ("1", "0")
)
def test_validate_in_config_format_valid(value):
    # No error thrown
    _BOOLEAN_VALIDATOR.validate_in_config_format(value)

@pytest.mark.parametrize(
    "value",
    (1, 0, "-1", "2", "True", "False", "", True, False, [], ["1"])
)
def test_validate_in_config_format_invalid(value):
    check error message
    with pytest.raises(ConfigFieldValueError):
        _BOOLEAN_VALIDATOR.validate_in_config_format(value)