import pytest

from lib.configs.format_converters import DiscreteFormatConverter


@pytest.mark.parametrize(
    "all_values, input, expected_output",
    (
        (("val1",), "0", "val1"),
        (("val1", "val2"), "0", "val1"),
        (("val1", "val2"), "1", "val2"),
    ),
)
def test_convert_to_python_format(all_values, input, expected_output):
    format_converter = DiscreteFormatConverter(all_values)
    assert format_converter.convert_to_python_format(input) == expected_output


@pytest.mark.parametrize(
    "all_values, input, expected_output",
    (
        (("val1",), "val1", "0"),
        (("val1", "val2"), "val1", "0"),
        (("val1", "val2"), "val2", "1"),
    ),
)
def test_convert_to_config_file_format(all_values, input, expected_output):
    format_converter = DiscreteFormatConverter(all_values)
    assert format_converter.convert_to_config_file_format(input) == expected_output
