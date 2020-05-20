import pytest

from resources.lib.configs import ConfigFieldValueError
from resources.lib.configs.validators import IntegerValidator


def _get_valid_params(min, max):
    return tuple((min, max, value) for value in range(min, max + 1))


_VALID_PARAMS = (
    _get_valid_params(0, 10) + _get_valid_params(-14, 123) + _get_valid_params(1, 1)
)

_INVALID_PARAMS = (
    (0, 0, -1),
    (0, 0, 1),
    (0, 10, 11),
    (3, 10, 2),
    (4, 7, -3),
    (4, 7, 50),
)


@pytest.mark.parametrize(
    "min, max, value", _VALID_PARAMS,
)
def test_validate_in_config_file_format_valid(min, max, value):
    validator = IntegerValidator(min, max)
    validator.validate_in_config_file_format(str(value))


@pytest.mark.parametrize("min, max, value", _INVALID_PARAMS)
def test_validate_in_config_file_format_invalid(min, max, value):
    validator = IntegerValidator(min, max)
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_config_file_format(str(value))
    assert str(value) in str(excinfo.value)
    assert ">= " + str(min) in str(excinfo.value)
    assert "<= " + str(max) in str(excinfo.value)


@pytest.mark.parametrize(
    "min, max, value", _VALID_PARAMS,
)
def test_validate_in_python_format_valid(min, max, value):
    validator = IntegerValidator(min, max)
    validator.validate_in_python_format(value)


@pytest.mark.parametrize("min, max, value", _INVALID_PARAMS)
def test_validate_in_python_format_invalid(min, max, value):
    validator = IntegerValidator(min, max)
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_python_format(value)
    assert str(value) in str(excinfo.value)
    assert ">= " + str(min) in str(excinfo.value)
    assert "<= " + str(max) in str(excinfo.value)
