"""Tests for configs.format_converters.BooleanFormatConverter"""
import pytest

from lib.configs.format_converters import BooleanFormatConverter

_BOOLEAN_FORMAT_CONVERTER = BooleanFormatConverter()


@pytest.mark.parametrize("input_value, expected_output", (("1", True), ("0", False)))
def test_convert_to_python_format(input_value, expected_output):
    """Ensures that string representations of booleans are correctly converted
    to booean values
    """
    assert (
        _BOOLEAN_FORMAT_CONVERTER.convert_to_python_format(input_value)
        == expected_output
    )


@pytest.mark.parametrize("input_value, expected_output", ((True, "1"), (False, "0")))
def test_convert_to_config_file_format(input_value, expected_output):
    """Ensures that booleans are correctly converted to their string
    representations
    """
    assert (
        _BOOLEAN_FORMAT_CONVERTER.convert_to_config_file_format(input_value)
        == expected_output
    )
