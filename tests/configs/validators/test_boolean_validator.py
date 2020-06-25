"""Tests for config.validators.BooleanValidator"""
import pytest
from lib.configs import ConfigFieldValueError
from lib.configs.validators import BooleanValidator

_BOOLEAN_VALIDATOR = BooleanValidator()


@pytest.mark.parametrize("value", (True, False))
def test_validate_in_python_format_valid(value):
    """Ensures that no errors are thrown when validating valid values in
    Python format
    """
    # No error thrown
    _BOOLEAN_VALIDATOR.validate_in_python_format(value)


@pytest.mark.parametrize("value", (1, 0, "1", "0", "True", "False", "", [], [True]))
def test_validate_in_python_format_invalid(value):
    """Ensures that a ConfigFieldValueError is raised for invalid values when
    validating in Python format
    """
    with pytest.raises(ConfigFieldValueError) as excinfo:
        _BOOLEAN_VALIDATOR.validate_in_python_format(value)
    assert str(value) in str(excinfo.value)


@pytest.mark.parametrize("value", ("1", "0"))
def test_validate_in_config_file_format_valid(value):
    """Ensures that no errors are thrown when validating valid values in
    config file format
    """
    # No error thrown
    _BOOLEAN_VALIDATOR.validate_in_config_file_format(value)


@pytest.mark.parametrize(
    "value", (1, 0, "-1", "2", "True", "False", "", True, False, [], ["1"])
)
def test_validate_in_config_file_format_invalid(value):
    """Ensures that a ConfigFieldValueError is raised for invalid values when
    validating in config file format
    """

    with pytest.raises(ConfigFieldValueError) as excinfo:
        _BOOLEAN_VALIDATOR.validate_in_config_file_format(value)
    assert str(value) in str(excinfo.value)
