import re
import sys
import os
import itertools
import pytest
import tempfile
from resources.lib.configs import IndBiosConfig, ConfigFieldValueError, ConfigFieldNameError

TEST_CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_configs")


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

def remove_comments_and_extra_white_space(file):
    useful_lines = set()
    comment_removal_regex = re.compile(";.*$")
    for line in file:
        line = comment_removal_regex.sub("", line).strip()
        if line:
            useful_lines.add(line)
    return useful_lines


def get_config_file_path(filename):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    return os.path.join(script_dir, "test_configs", filename)


class TestIndBiosConfig:
    @classmethod
    def setup_class(cls):
        cls._config = IndBiosConfig()

    @pytest.mark.parametrize(
            "filename", 
            ["valid1.cfg"]
    )
    def test_parse_valid_config(self, filename):
        filename = get_config_file_path(filename)
        self._config.read(filename)

    @pytest.mark.parametrize("filename, field_that_is_reset, other_fields_that_should_not_be_reset",[
        ("invalid_boolean.cfg", "AUTOLOADDVD", {"AVCHECK": False})
    ])
    def test_parse_invalid_field_reset_to_default(self, filename, field_that_is_reset, other_fields_that_should_not_be_reset):
        filename = get_config_file_path(filename)
        self._config.read(filename, True)
        # Ensure that this value is reset to default as it was invalid
        assert self._config.get(field_that_is_reset) == self._config.defaults()[field_that_is_reset], field_that_is_reset + " reset to default value"
        # Ensure that these values were not reset to default
        for field in other_fields_that_should_not_be_reset:
            expected_value = other_fields_that_should_not_be_reset[field]
            assert self._config.get(field) == expected_value, field+" has default value"

    @pytest.mark.parametrize("filename", [
        "invalid_camera_view.cfg",
        "invalid_model_extension.cfg",
        "invalid_xbe_extension.cfg",
        "invalid_bmp_extension.cfg",
        "invalid_boolean.cfg"
    ])
    def test_parse_invalid(self, filename):
        with pytest.raises(ConfigFieldValueError):
            filename = get_config_file_path(filename)
            self._config.read(filename, False)

    @pytest.mark.parametrize("filename", os.listdir(TEST_CONFIG_DIR))
    def test_config_file_output_no_changes(self, filename):
        filename = get_config_file_path(filename)
        self._config.read(filename, True)
        with tempfile.TemporaryFile() as written_file_pointer:
            self._config.write(written_file_pointer)
            written_file_pointer.seek(os.SEEK_SET)
            
            new_config = IndBiosConfig()
            new_config.readfp(written_file_pointer, True)

            for option in self._config.options():
                assert self._config.get(option) == new_config.get(option), option + " has the same value"



    @pytest.mark.parametrize("option,value", [
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
        ("DASH3", "G:\\test\\test\\xboxdash.xbe")
    ])
    def test_set_value_valid(self, option, value):
        self._config.set(option, value)
        assert self._config.get(option) == value, "value set correctly"

    @pytest.mark.parametrize("option,value", [
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
        ("FOG1CUSTOM", "1")
    ])
    def test_set_value_invalid(self, option, value):
        old_value = self._config.get(option)
        with pytest.raises(ConfigFieldValueError):
            self._config.set(option, value)

        assert self._config.get(option) == old_value, "value not changed"

    @pytest.mark.parametrize("preset_filename,apply_to_fields",itertools.product(os.listdir(TEST_CONFIG_DIR), sub_lists(list(IndBiosConfig().options()))))
    def test_load_preset(self, preset_filename, apply_to_fields):
        preset_filename = get_config_file_path(preset_filename)
        values_before = {option: self._config.get(option) for option in self._config.options()}
        preset_config = IndBiosConfig()
        preset_config.read(preset_filename, True)
        self._config.load_preset(preset_filename, apply_to_fields)

        # Ideally I would I use subtest here so that if one assert fails the others will still be executed.
        # Unfortunately subtest is not available in pytest. The other alternative would be to use parameterized to
        # perform a separate test for each field but that would be really slow.
        for field in self._config.options():
            new_field_value = self._config.get(field)
            if field in apply_to_fields:
                assert new_field_value == preset_config.get(field), field + " value changed to the one from the preset"
            else:
                assert new_field_value == values_before[field], field + " value unchanged"
