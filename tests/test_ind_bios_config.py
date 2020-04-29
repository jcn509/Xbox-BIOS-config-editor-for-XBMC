import re
import sys
import os
import itertools
import pytest
from StringIO import StringIO
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


class TestIndBiosConfig:
    @classmethod
    def setup_class(cls):
        cls._config = IndBiosConfig()

    @pytest.mark.parametrize(
            "filename", 
            [("valid1.cfg",)]
    )
    def test_parse_valid_config(self, filename):
        self._config.read(filename)

    @pytest.mark.parametrize("filename, field_that_is_reset, other_fields_that_should_not_be_reset",[
        ("invalid_boolean.cfg", "AUTOLOADDVD", {"AVCHECK": "0"})
    ])
    def test_parse_invalid_field_reset_to_default(self, filename, field_that_is_reset, other_fields_that_should_not_be_reset):
        self._config.read(filename, True)
        # Ensure that this value is reset to default as it was invalid
        assert self._config.get(field_that_is_reset) == self._config.defaults()[field_that_is_reset], field_that_is_reset + " reset to default value"
        # Ensure that these values were not reset to default
        for field in other_fields_that_should_not_be_reset:
            expected_value = other_fields_that_should_not_be_reset[field]
            assert self._config.get(field) == expected_value, field+" has default value"

    # @pytest.mark.parametrize("filename", [
    #     ("invalid_camera_view.cfg",),
    #     ("invalid_model_extension.cfg",),
    #     ("invalid_xbe_extension.cfg",),
    #     ("invalid_bmp_extension.cfg",),
    #     ("invalid_boolean.cfg",)
    # ])
    # def test_parse_invalid(self, filename):
    #     with self.assertRaises(ValueError):
    #         self._config.read(filename, False)

    # @pytest.mark.parametrize("filename", os.listdir(TEST_CONFIG_DIR))
    # def test_config_file_output_no_changes(self, filename):
    #     self._config.readv(filename, True)
    #     fp = StringIO()
    #     fields_and_value = {}
    #     defaults = self._config.defaults()
    #     for field, value in self._config.items():
    #         fields_and_value[field] = value
    #     self._config.write(fp)
    #     fp.seek(0, 0)
    #     output_values = {}
    #     valid_fields = defaults.keys()
    #     for line in fp:
    #         if line[-2:] == "\r\n":
    #             line = line[:-2]
    #         elif line[-1] == "\n":
    #             line = line[:-1]

    #         if len(line) >= 2:
    #             if line[0] == "[" and line[-1] == "]":
    #                 raise ValueError("Section in file: " + line)

    #             field, value = line.split(" = ")
    #             if re.search(r"\s", value):
    #                 if not (value[0] == '"' and value[-1] == '"'):
    #                     raise ValueError("Value " + value + " for field " + field +
    #                                      " contains whitespace but is not wrapped in " + '"')

    #             # Don't care about extra fields that may or may not be output (i.e. extra fields in some input cfg)
    #             if field in valid_fields:
    #                 output_values[field] = value

    #     for field in valid_fields:
    #         config_value = fields_and_value[field]
    #         default_value = defaults[field]
    #         if config_value == default_value:
    #             if field in output_values:
    #                 output_value = output_values[field]
    #                 raise ValueError(output_value + " output for " + field + " when " +
    #                                  output_value + " is the default. Config value is " + config_value)
    #         else:
    #             if field not in output_values:
    #                 raise ValueError(config_value + " not output for " + field + " when " +
    #                                  config_value + " is non-default. Default is " + default_value)
    #             else:
    #                 output_value = output_values[field]
    #                 if config_value != output_value:
    #                     raise ValueError(output_value + " output for " + field + " instead of " + config_value)





    # @pytest.mark.parametrize("option,value", [
    #     ("TMS", "0"),
    #     ("TMS", "1"),
    #     ("CUSTOMBLOB", "0"),
    #     ("FOG1CUSTOM", "0"),
    #     ("FOG1CUSTOM", "1"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition6\\avalaunch.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition6\\avalaunch.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition6\\avalaunch.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition7\\xboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition7\\xboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition7\\xboxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition7\\dir\\xboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition7\\dir1\\dir2\\xboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition7\\test\\test\\xboxdash.xbe")
    # ])
    # def test_set_value_valid(self, option, value):
    #     self._config.set(option, value)
    #     assert self._config.get(option) == value, "value set correctly"

    # @pytest.mark.parametrize("option,value", [
    #     ("TMS", "GGGG"),
    #     ("TMS", "X"),
    #     ("CUSTOMBLOB", "3"),
    #     ("CUSTOMBLOB", "C:\\blob.x"),
    #     ("DASH1", "C:\\dash.xbe"),
    #     ("DASH2", "C:\\dash.xbe"),
    #     ("DASH3", "C:\\dash.xbe"),
    #     ("DASH1", "E:\\evoxdash.xbe"),
    #     ("DASH2", "E:\\evoxdash.xbe"),
    #     ("DASH3", "E:\\evoxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"),
    #     ("DASH1", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"),
    #     ("DASH2", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"),
    #     ("DASH3", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"),
    #     ("DASH1", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
    #     ("DASH2", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
    #     ("DASH3", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"),
    #     ("FOG1CUSTOM", "a"),
    #     ("FOG1CUSTOM", "2")
    # ])
    # def test_set_value_invalid(self, option, value):
    #     old_value = self._config.get(option)
    #     with self.assertRaises(ValueError):
    #         self._config.set(option, value)

    #     assert self._config.get(option) == old_value, "value not changed"

    # @pytest.mark.parametrize("preset_filename,apply_to_fields",itertools.product(os.listdir(TEST_CONFIG_DIR), sub_lists(list(IndBiosConfig().options()))))
    # def test_load_preset(self, preset_filename, apply_to_fields):
    #     values_before = dict(self._config.items())
    #     preset_config = IndBiosConfig()
    #     self._read_config_for_obj(preset_config, preset_filename, True)
    #     self._config.load_preset(os.path.join(TEST_CONFIG_DIR, preset_filename), apply_to_fields)

    #     # Ideally I would I use subtest here so that if one assert fails the others will still be executed.
    #     # Unfortunately subtest is not available in pytest. The other alternative would be to use parameterized to
    #     # perform a separate test for each field but that would be really slow.
    #     for field in self._config.options():
    #         try:
    #             new_field_value = self._config.get(field)
    #             if field in apply_to_fields:
    #                 assert new_field_value == preset_config.get(field), field + " value changed to the one from the preset"
    #             else:
    #                 assert new_field_value == values_before[field], field + " value unchanged"
    #         except ConfigFieldNameError:
    #             pass # Don't care about nonsense fields
