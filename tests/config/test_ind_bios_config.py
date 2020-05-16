import re
import sys
import os
import pytest
import tempfile
from resources.lib.configs import (
    IndBiosConfig,
    ConfigFieldValueError,
    ConfigFieldNameError,
)

TEST_CONFIG_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "test_configs"
)
DEFAULT_CONFIG = IndBiosConfig()
CONFIG_OPTIONS = DEFAULT_CONFIG.options()
CONFIG_DEFAULTS = {option: DEFAULT_CONFIG.get(option) for option in CONFIG_OPTIONS}


def sub_lists(list1):
    # store all the sublists
    sublists = [[]]

    # first loop
    for i in range(len(list1) + 1):

        # second loop
        for j in range(i + 1, len(list1) + 1):
            # slice the subarray
            sub = list1[i:j]
            sublists.append(sub)

    return sublists


def get_config_file_path(filename):
    return os.path.join(TEST_CONFIG_DIR, filename)


def get_config_editor_for_file(filename):
    config_editor = IndBiosConfig()
    config_editor.read(filename)
    return config_editor


def get_config_editors_for_each_file(filenames):
    config_editors = []
    for filename in filenames:
        config_editor = get_config_editor_for_file(filename)
        config_editors.append(config_editor)
    return config_editors


ALL_CONFIG_FILES = tuple(
    [get_config_file_path(file) for file in os.listdir(TEST_CONFIG_DIR)]
)


@pytest.mark.parametrize("filename", ["valid1.cfg"])
def test_parse_valid_config_no_errors(filename):
    filename = get_config_file_path(filename)
    IndBiosConfig().read(filename)


@pytest.mark.parametrize(
    "filename, field_that_is_reset, other_fields_that_should_not_be_reset",
    [("invalid_boolean.cfg", "AUTOLOADDVD", {"AVCHECK": False})],
)
def test_parse_invalid_field_reset_to_default(
    filename, field_that_is_reset, other_fields_that_should_not_be_reset
):
    config = IndBiosConfig()
    filename = get_config_file_path(filename)
    config.read(filename, True)
    # Ensure that this value is reset to default as it was invalid
    assert config.get(field_that_is_reset) == config.defaults()[field_that_is_reset], (
        field_that_is_reset + " reset to default value"
    )
    # Ensure that these values were not reset to default
    for field in other_fields_that_should_not_be_reset:
        expected_value = other_fields_that_should_not_be_reset[field]
        assert config.get(field) == expected_value, field + " has default value"


@pytest.mark.parametrize(
    "filename",
    [
        "invalid_camera_view.cfg",
        "invalid_model_extension.cfg",
        "invalid_xbe_extension.cfg",
        "invalid_bmp_extension.cfg",
        "invalid_boolean.cfg",
    ],
)
def test_parse_invalid(filename):
    config = IndBiosConfig()
    with pytest.raises(ConfigFieldValueError):
        filename = get_config_file_path(filename)
        config.read(filename, False)


@pytest.mark.parametrize("config", get_config_editors_for_each_file(ALL_CONFIG_FILES))
def test_config_file_output_no_changes(config):
    with tempfile.TemporaryFile() as written_file_pointer:
        config.write(written_file_pointer)
        written_file_pointer.seek(os.SEEK_SET)

        new_config = IndBiosConfig()
        new_config.readfp(written_file_pointer, True)

        for option in CONFIG_OPTIONS:
            assert config.get(option) == new_config.get(option), (
                option + " has the same value"
            )


@pytest.mark.parametrize(
    "option,value",
    [
        ("TMS", False),
        ("TMS", True),
        ("CUSTOMBLOB", None),
        ("FOG1CUSTOM", False),
        ("FOG1CUSTOM", True),
        ("DASH1", "E:\\evoxdash.xbe"),
        ("DASH2", "E:\\evoxdash.xbe"),
        ("DASH3", "E:\\evoxdash.xbe"),
        ("DASH1", "C:\\yboxdash.xbe"),
        ("DASH2", "C:\\yboxdash.xbe"),
        ("DASH3", "C:\\yboxdash.xbe"),
        ("DASH1", "F:\\avalaunch.xbe"),
        ("DASH2", "F:\\avalaunch.xbe"),
        ("DASH3", "F:\\avalaunch.xbe"),
        ("DASH1", "G:\\xboxdash.xbe"),
        ("DASH2", "G:\\xboxdash.xbe"),
        ("DASH3", "G:\\xboxdash.xbe"),
        ("DASH1", "G:\\dir\\xboxdash.xbe"),
        ("DASH2", "G:\\dir1\\dir2\\xboxdash.xbe"),
        ("DASH3", "G:\\test\\test\\xboxdash.xbe"),
    ],
)
def test_set_value_valid(option, value):
    config = IndBiosConfig()
    config.set(option, value)
    assert config.get(option) == value, "value set correctly"


@pytest.mark.parametrize(
    "option,value",
    [
        ("TMS", "GGGG"),
        ("TMS", "X"),
        ("CUSTOMBLOB", "3"),
        ("CUSTOMBLOB", "A:\\blob.x"),
        ("DASH1", "B:\\dash.xbe"),
        ("DASH2", "D:\\dash.xbe"),
        ("DASH3", "X:\\dash.xbe"),
        ("DASH1", "Y:\\evoxdash.xbe"),
        ("DASH2", "Z:\\evoxdash.xbe"),
        ("DASH3", "Q:\\evoxdash.xbe"),
        ("DASH1", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"),
        ("DASH2", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"),
        ("DASH3", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"),
        ("DASH1", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"),
        ("DASH2", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"),
        ("DASH3", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"),
        ("DASH1", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"),
        ("DASH2", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"),
        ("DASH3", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"),
        ("DASH1", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"),
        ("DASH2", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"),
        ("DASH3", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"),
        ("DASH1", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"),
        ("DASH2", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"),
        ("DASH3", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"),
        ("DASH1", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"),
        ("DASH2", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"),
        ("DASH3", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"),
        ("DASH1", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
        ("DASH2", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
        ("DASH3", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
        ("FOG1CUSTOM", "a"),
        ("FOG1CUSTOM", "2"),
        ("FOG1CUSTOM", None),
        ("FOG1CUSTOM", "1"),
    ],
)
def test_set_value_invalid(option, value):
    config = IndBiosConfig()
    old_value = config.get(option)
    with pytest.raises(ConfigFieldValueError):
        config.set(option, value)

    assert config.get(option) == old_value, "value not changed"


@pytest.mark.parametrize(
    "preset_filename,preset_config,apply_to_fields",
    [
        (filename, get_config_editor_for_file(filename), apply_to_fields)
        for filename in ALL_CONFIG_FILES
        for apply_to_fields in sub_lists(list(CONFIG_OPTIONS))
    ],
)
def test_load_preset(preset_filename, preset_config, apply_to_fields):
    config = IndBiosConfig()
    config.load_preset(preset_filename, apply_to_fields)

    # Ideally I would I use subtest here so that if one assert fails the others will still be executed.
    # Unfortunately subtest is not available in pytest. The other alternative would be to use parameterized to
    # perform a separate test for each field but that would be really slow.
    for field in CONFIG_OPTIONS:
        new_field_value = config.get(field)
        if field in apply_to_fields:
            assert new_field_value == preset_config.get(field), (
                field + " value changed to the one from the preset"
            )
        else:
            assert new_field_value == CONFIG_DEFAULTS[field], field + " value unchanged"
