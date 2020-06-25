"""Tests for configs.validators.ColourValidator and
configs.validators.ColourWithAlphaValidator

Note for colours the Python and config file formats are the same
"""
import pytest
from lib.configs import ConfigFieldValueError
from lib.configs.validators import ColourValidator, ColourWithAlphaValidator

_COLOUR_VALIDATOR = ColourValidator()
_COLOUR_WITH_ALPHA_VALIDATOR = ColourWithAlphaValidator()

_VALID_COLOURS_NO_ALPHA = ("0xFFFFFF", "0x123456", "0x000000")
_INVALID_COLOURS = (
    True,
    False,
    1,
    3,
    4.5,
    "green",
    "RED",
    "FFFFFF",
    "RBG(255,255,255)",
    "0x0000000G",
    "0xFFFFFG",
    "0xZZZZZZ",
    "FFFFFFFF",
    "RBGA(255,255,255,255)",
)
_VALID_COLOURS_WITH_ALPHA = ("0xFFFFFFFF", "0x00000000", "0x12345678")


@pytest.mark.parametrize("value", _VALID_COLOURS_NO_ALPHA)
def test_validate_colour_in_python_format_valid(value):
    """Ensures that no errors are thrown when validating valid colours in
    Python format
    """
    # No error thrown
    _COLOUR_VALIDATOR.validate_in_python_format(value)


@pytest.mark.parametrize("value", _VALID_COLOURS_NO_ALPHA)
def test_validate_colour_in_config_format_valid(value):
    """Ensures that no errors are thrown when validating valid colours in
    config file format
    """
    # No error thrown
    _COLOUR_VALIDATOR.validate_in_config_file_format(value)


@pytest.mark.parametrize("value", _INVALID_COLOURS + _VALID_COLOURS_WITH_ALPHA)
def test_validate_colour_in_python_format_invalid(value):
    """Ensures that a ConfigFieldValueError is raised when validating invalid
    colours in Python format
    """
    with pytest.raises(ConfigFieldValueError) as excinfo:
        _COLOUR_VALIDATOR.validate_in_python_format(value)
    assert str(value) in str(excinfo.value)


@pytest.mark.parametrize("value", _INVALID_COLOURS + _VALID_COLOURS_WITH_ALPHA)
def test_validate_colour_in_config_format_invalid(value):
    """Ensures that a ConfigFieldValueError is raised when validating invalid
    colours in config file format
    """
    with pytest.raises(ConfigFieldValueError) as excinfo:
        _COLOUR_VALIDATOR.validate_in_config_file_format(value)
    assert str(value) in str(excinfo.value)


@pytest.mark.parametrize("value", _VALID_COLOURS_WITH_ALPHA)
def test_validate_colour_in_python_format_valid(value):
    """Ensures that no errors are thrown when validating valid colours with
    alpha components in Python format
    """
    # No error thrown
    _COLOUR_WITH_ALPHA_VALIDATOR.validate_in_python_format(value)


@pytest.mark.parametrize("value", _VALID_COLOURS_WITH_ALPHA)
def test_validate_colour_in_config_format_valid(value):
    """Ensures that no errors are thrown when validating valid colours with
    alpha components in config file format
    """
    # No error thrown
    _COLOUR_WITH_ALPHA_VALIDATOR.validate_in_config_file_format(value)


@pytest.mark.parametrize("value", _INVALID_COLOURS + _VALID_COLOURS_NO_ALPHA)
def test_validate_colour_in_python_format_invalid(value):
    """Ensures that a ConfigFieldValueError is raised when validating invalid
    colours with alpha components in Python Format
    """
    with pytest.raises(ConfigFieldValueError) as excinfo:
        _COLOUR_WITH_ALPHA_VALIDATOR.validate_in_python_format(value)
    assert str(value) in str(excinfo.value)


@pytest.mark.parametrize("value", _INVALID_COLOURS + _VALID_COLOURS_NO_ALPHA)
def test_validate_colour_in_config_format_invalid(value):
    """Ensures that a ConfigFieldValueError is raised when validating invalid
    colours with alpha components in config file Format
    """
    with pytest.raises(ConfigFieldValueError) as excinfo:
        _COLOUR_WITH_ALPHA_VALIDATOR.validate_in_config_file_format(value)
    assert str(value) in str(excinfo.value)
