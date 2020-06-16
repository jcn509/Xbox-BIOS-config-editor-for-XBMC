import pytest

from lib.configs.format_converters import BooleanFormatConverter

_BOOLEAN_FORMAT_CONVERTER = BooleanFormatConverter()


@pytest.mark.parametrize("input, expected_output", (("1", True), ("0", False)))
def test_convert_to_python_format(input, expected_output):
    assert _BOOLEAN_FORMAT_CONVERTER.convert_to_python_format(input) == expected_output


@pytest.mark.parametrize("input, expected_output", ((True, "1"), (False, "0")))
def test_convert_to_config_file_format(input, expected_output):
    assert (
        _BOOLEAN_FORMAT_CONVERTER.convert_to_config_file_format(input)
        == expected_output
    )
