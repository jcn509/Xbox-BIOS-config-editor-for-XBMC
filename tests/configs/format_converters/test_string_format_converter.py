"""Tests for configs.format_converters.StringFormatConverter

This converter should do absolutely nothing to its inputs...
"""

import pytest

from lib.configs.format_converters import StringFormatConverter

_STRING_VALUES = ("test", "String", "GGGG", "one")


@pytest.mark.parametrize(
    "string_value", _STRING_VALUES,
)
def test_convert_to_python_format(string_value):
    """Tests that the return value is the same as the input"""
    format_converter = StringFormatConverter()
    assert format_converter.convert_to_python_format(string_value) == string_value


@pytest.mark.parametrize(
    "string_value", _STRING_VALUES,
)
def test_convert_to_config_file_format(string_value):
    """Tests that the return value is the same as the input"""
    format_converter = StringFormatConverter()
    assert format_converter.convert_to_config_file_format(string_value) == string_value
