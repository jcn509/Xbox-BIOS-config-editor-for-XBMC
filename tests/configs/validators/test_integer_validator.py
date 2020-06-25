"""Tests for configs.validators.IntegerValidator"""
import pytest

from lib.configs import ConfigFieldValueError
from lib.configs.validators import IntegerValidator


def _get_valid_params(min_value, max_value):
    """:returns: a tuple of tuples of the for
    (min_value, max_value, some_value_to_test)
    for all values to test that are >= min_value and <= max_value
    """
    return tuple(
        (min_value, max_value, value) for value in range(min_value, max_value + 1)
    )


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
    "min_value, max_value, value", _VALID_PARAMS,
)
def test_validate_in_config_file_format_valid(min_value, max_value, value):
    """Ensures that no exceptions are thrown when validating valid integers in
    config file format
    """
    validator = IntegerValidator(min_value, max_value)
    validator.validate_in_config_file_format(str(value))


@pytest.mark.parametrize("min_value, max_value, value", _INVALID_PARAMS)
def test_validate_in_config_file_format_invalid(min_value, max_value, value):
    """Ensures that a ConfigFieldValueError is raised when validating invalid
    values in config file format
    """
    validator = IntegerValidator(min_value, max_value)
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_config_file_format(str(value))
    assert str(value) in str(excinfo.value)
    assert ">= " + str(min_value) in str(excinfo.value)
    assert "<= " + str(max_value) in str(excinfo.value)


@pytest.mark.parametrize(
    "min_value, max_value, value", _VALID_PARAMS,
)
def test_validate_in_python_format_valid(min_value, max_value, value):
    """Ensures that no exceptions are thrown when validating valid integers in
    Python format
    """
    validator = IntegerValidator(min_value, max_value)
    validator.validate_in_python_format(value)


@pytest.mark.parametrize("min_value, max_value, value", _INVALID_PARAMS)
def test_validate_in_python_format_invalid(min_value, max_value, value):
    """Ensures that a ConfigFieldValueError is raised when validating invalid
    values in Python format
    """
    validator = IntegerValidator(min_value, max_value)
    with pytest.raises(ConfigFieldValueError) as excinfo:
        validator.validate_in_python_format(value)
    assert str(value) in str(excinfo.value)
    assert ">= " + str(min_value) in str(excinfo.value)
    assert "<= " + str(max_value) in str(excinfo.value)
