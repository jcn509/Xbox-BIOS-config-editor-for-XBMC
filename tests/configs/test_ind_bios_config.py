"""Tests for the IndBiosConfig class"""
import re
import sys
import os
import pytest
import tempfile
from lib.configs import (
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
    """:returns: all possible sublists for the input"""
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
    """:returns: the full path for a given test config file"""
    return os.path.join(TEST_CONFIG_DIR, filename)


def get_config_editor_for_file(filename, **kwargs):
    """:returns: an IndBiosConfig instance that is using the values specified\
            for all fields that are defined in filename and default values\
            for all the other fields
    """
    filename = get_config_file_path(filename)
    config_editor = IndBiosConfig()
    with open(filename, "r") as config_file:
        config_editor.read(config_file, **kwargs)
    return config_editor


def get_config_editors_for_each_file(filenames):
    """:returns: a list of IndBiosConfig one for each file in filenames"""
    return [get_config_editor_for_file(filename) for filename in filenames]


ALL_CONFIG_FILES = tuple(os.listdir(TEST_CONFIG_DIR))


@pytest.mark.parametrize("filename", ("valid1.cfg", "valid2.cfg"))
def test_parse_valid_config_no_errors(filename):
    """Ensures that no exceptions are thrown when parsing a valid config"""
    get_config_editor_for_file(filename)


@pytest.mark.parametrize(
    "filename, field_that_is_reset, other_fields_that_should_not_be_reset",
    [("invalid_boolean.cfg", "AUTOLOADDVD", {"AVCHECK": False})],
)
def test_parse_invalid_field_reset_to_default(
    filename, field_that_is_reset, other_fields_that_should_not_be_reset
):
    """Ensures that invalid fields are set to default when read from a file
    if they are supposed to be
    """
    config = get_config_editor_for_file(filename, set_invalid_fields_to_default=True)
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
    (
        "invalid_camera_view.cfg",
        "invalid_model_extension.cfg",
        "invalid_xbe_extension.cfg",
        "invalid_bmp_extension.cfg",
        "invalid_boolean.cfg",
    ),
)
def test_parse_invalid(filename):
    """Ensures that an exception is thrown when parsing an invalid config file
    if it is supposed to be
    """
    with pytest.raises(ConfigFieldValueError):
        get_config_editor_for_file(filename, set_invalid_fields_to_default=False)    


@pytest.mark.parametrize("config", get_config_editors_for_each_file(ALL_CONFIG_FILES))
def test_config_file_output_no_changes(config):
    """A config file is read by IndBiosConfig then a copy is written to disk.
    This test ensures that both files contain the same values
    """
    with tempfile.TemporaryFile() as written_file_pointer:
        config.write(written_file_pointer)
        written_file_pointer.seek(os.SEEK_SET)

        new_config = IndBiosConfig()
        new_config.read(written_file_pointer, True)

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
    """Ensures that valid values are set correctly"""
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
    """Ensures that exceptions are thrown when trying to set invalid values
    and that the value is not actually set
    """
    config = IndBiosConfig()
    old_value = config.get(option)
    with pytest.raises(ConfigFieldValueError):
        config.set(option, value)

    assert config.get(option) == old_value, "value not changed"



_PRESET_PARAMETERS = tuple(
    (get_config_file_path(filename), get_config_editor_for_file(filename), apply_to_fields)
    for filename in ALL_CONFIG_FILES
    for apply_to_fields in sub_lists(list(CONFIG_OPTIONS))
)


@pytest.mark.parametrize(
    "preset_filename,preset_config,apply_to_fields",
    _PRESET_PARAMETERS
)
def test_load_preset(preset_filename, preset_config, apply_to_fields):
    """Ensures that presets can be loaded and the values will only be applied
    to the fields that they are meant to be applied to
    """
    config = IndBiosConfig()
    with open(preset_filename, "r") as preset_file:
        config.load_preset(preset_file, apply_to_fields)

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


@pytest.mark.parametrize(
    "preset_filename,config,fields_to_save",
    _PRESET_PARAMETERS
)
def test_save_preset(preset_filename, config, fields_to_save):
    """Ensures that presets can be saved and only the values we are interested
    in will be saved
    """
    with tempfile.TemporaryFile() as written_file_pointer:
        config.save_preset(written_file_pointer, fields_to_save)
        written_file_pointer.seek(os.SEEK_SET)

        new_config = IndBiosConfig()
        new_config.read(written_file_pointer)

        # Ideally I would I use subtest here so that if one assert fails the others will still be executed.
        # Unfortunately subtest is not available in pytest. The other alternative would be to use parameterized to
        # perform a separate test for each field but that would be really slow.
        for field in CONFIG_OPTIONS:
            new_field_value = new_config.get(field)
            # These fields are tested elsewhere and were causing headaches
            if field not in config._get_true_if_fields_dont_have_values():
                if field in fields_to_save:
                    assert new_field_value == config.get(field), (
                        field + " value changed to the one from the preset"
                    )
                else:
                    assert new_field_value == CONFIG_DEFAULTS[field], field + " value unchanged"

