from itertools import product

import pytest

from resources.lib.configs.format_converters import (
    DOSFilePathFormatConverter,
    OptionalDOSFilePathFormatConverter,
)

_CONFIG_AND_PYTHON_PATHS = (
    (
        "\\Device\\Harddisk0\\Partition2\\flubber.x",
        "C:\\flubber.x",
    ),
    (
        "\\Device\\Harddisk0\\Partition1\\test\\default.xbe",
        "E:\\test\\default.xbe"
    ),
    (
        "\\Device\\Harddisk0\\Partition6\\one\\two\\TEST.bmp",
        "F:\\one\\two\\TEST.bmp"
    ),
    (
        "\\Device\\Harddisk0\\Partition7\\asdasd\\default1.xbe",
        "G:\\asdasd\\default1.xbe"
    )
)

_CONVERTERS_AND_PATHS = tuple(
    (converter,) + python_and_config_value
    for python_and_config_value in _CONFIG_AND_PYTHON_PATHS
    for converter in (DOSFilePathFormatConverter, OptionalDOSFilePathFormatConverter)
) + ((OptionalDOSFilePathFormatConverter, "0", None), )


@pytest.mark.parametrize("converter, config_path, expected_python_path", _CONVERTERS_AND_PATHS)
def test_convert_to_python_format(converter, config_path, expected_python_path):
    format_converter = converter()
    assert (
        format_converter.convert_to_python_format(config_path) == expected_python_path
    )


# Notice that the parameters are the other way around
@pytest.mark.parametrize("converter, expected_config_path, python_path", _CONVERTERS_AND_PATHS)
def test_convert_to_config_file_format(converter, expected_config_path, python_path):
    format_converter = converter()
    assert (
        format_converter.convert_to_config_file_format(python_path)
        == expected_config_path
    )
