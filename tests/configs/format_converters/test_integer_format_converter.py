import pytest

from lib.configs.format_converters import IntegerFormatConverter


@pytest.mark.parametrize(
    "integer_value",
    tuple(range(-10, 10))
)
def test_convert_to_python_format(integer_value):
    format_converter = IntegerFormatConverter()
    assert format_converter.convert_to_python_format(str(integer_value)) == integer_value


@pytest.mark.parametrize(
    "integer_value",
    tuple(range(-10,10)),
)
def test_convert_to_config_file_format(integer_value):
    format_converter = IntegerFormatConverter()
    assert format_converter.convert_to_config_file_format(integer_value) == str(integer_value)
