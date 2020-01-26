import re
import sys
import os
import itertools
from StringIO import StringIO

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, os.path.join("..", "script.ind_bios_config_editor", "resources", "lib"))
from configs import IndBiosConfig

import unittest
from parameterized import parameterized

TEST_CONFIG_DIR = "test_configs"

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


class TestIndBiosConfig(unittest.TestCase):

    def setUp(self):
        self.config = IndBiosConfig()

    def _read_config(self, config_filename, set_invalid_fields_to_default=False):
        self._read_config_for_obj(self.config, config_filename, set_invalid_fields_to_default)

    def _read_config_for_obj(self, config_obj, config_filename, set_invalid_fields_to_default=False):
        config_obj.read(os.path.join(TEST_CONFIG_DIR, config_filename),
                        set_invalid_fields_to_default=set_invalid_fields_to_default)

    @parameterized.expand([
        ["valid1.cfg"]
    ])
    def test_parse_valid_config(self, filename):
        self._read_config(filename)

    def get(self, config, field):
        return config.get(config.get_default_section(), field)

    def set(self, config, field, value):
        config.set(config.get_default_section(), field, value)

    @parameterized.expand([
        ["invalid_boolean.cfg", "AUTOLOADDVD", {"AVCHECK": "0"}]
    ])
    def test_parse_invalid_field_reset_to_default(self, filename, field_that_is_reset,
                                                  other_fields_that_should_not_be_reset):
        self._read_config(filename, True)
        # Ensure that this value is reset to default as it was invalid
        self.assertEqual(self.get(self.config, field_that_is_reset),
                         self.config.defaults()[self.config.get_default_section()][field_that_is_reset])
        # Ensure that these values were not reset to default
        for field in other_fields_that_should_not_be_reset:
            expected_value = other_fields_that_should_not_be_reset[field]
            self.assertEqual(self.get(self.config, field), expected_value)

    @parameterized.expand([
        ["invalid_camera_view.cfg"],
        ["invalid_model_extension.cfg"],
        ["invalid_xbe_extension.cfg"],
        ["invalid_bmp_extension.cfg"],
        ["invalid_boolean.cfg"]
    ])
    def test_parse_invalid(self, filename):
        with self.assertRaises(ValueError):
            self._read_config(filename, False)

    @parameterized.expand(os.listdir(TEST_CONFIG_DIR))
    def test_config_file_output_no_changes(self, filename):
        self._read_config(filename, True)
        fp = StringIO()
        fields_and_value = {}
        default_section = self.config.get_default_section()
        defaults = self.config.defaults()
        for field, value in self.config.items(default_section):
            fields_and_value[field] = value
        self.config.write(fp)
        fp.seek(0, 0)
        output_values = {}
        valid_fields = defaults[default_section].keys()
        for line in fp:
            if line[-2:] == "\r\n":
                line = line[:-2]
            elif line[-1] == "\n":
                line = line[:-1]

            if len(line) >= 2:
                if line[0] == "[" and line[-1] == "]":
                    raise ValueError("Section in file: " + line)

                field, value = line.split(" = ")
                if re.search(r"\s", value):
                    if not (value[0] == '"' and value[-1] == '"'):
                        raise ValueError("Value " + value + " for field " + field +
                                         " contains whitespace but is not wrapped in " + '"')

                # Don't care about extra fields that may or may not be output (i.e. extra fields in some input cfg)
                if field in valid_fields:
                    output_values[field] = value

        for field in valid_fields:
            config_value = fields_and_value[field]
            default_value = defaults[default_section][field]
            if config_value == default_value:
                if field in output_values:
                    output_value = output_values[field]
                    raise ValueError(output_value + " output for " + field + " when " +
                                     output_value + " is the default. Config value is " + config_value)
            else:
                if field not in output_values:
                    raise ValueError(config_value + " not output for " + field + " when " +
                                     config_value + " is non-default. Default is " + default_value)
                else:
                    output_value = output_values[field]
                    if config_value != output_value:
                        raise ValueError(output_value + " output for " + field + " instead of " + config_value)





    @parameterized.expand([
        ["TMS", "0"],
        ["TMS", "1"],
        ["CUSTOMBLOB", "0"],
        ["FOG1CUSTOM", "0"],
        ["FOG1CUSTOM", "1"],
        ["DASH1", "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition1\\yboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition1\\yboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition1\\yboxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition6\\avalaunch.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition6\\avalaunch.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition6\\avalaunch.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition7\\xboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition7\\xboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition7\\xboxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition7\\dir\\xboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition7\\dir1\\dir2\\xboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition7\\test\\test\\xboxdash.xbe"],
    ])
    def test_set_value_valid(self, option, value):
        self.set(self.config, option, value)
        self.assertEquals(self.get(self.config, option), value)

    @parameterized.expand([
        ["TMS", "GGGG"],
        ["TMS", "X"],
        ["CUSTOMBLOB", "3"],
        ["CUSTOMBLOB", "C:\\blob.x"],
        ["DASH1", "C:\\dash.xbe"],
        ["DASH2", "C:\\dash.xbe"],
        ["DASH3", "C:\\dash.xbe"],
        ["DASH1", "E:\\evoxdash.xbe"],
        ["DASH2", "E:\\evoxdash.xbe"],
        ["DASH3", "E:\\evoxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition0\\xboxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition3\\xboxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition4\\xboxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition5\\xboxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk0\\Partition8\\xboxdash.xbe"],
        ["DASH1", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"],
        ["DASH2", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"],
        ["DASH3", "\\Device\\Harddisk1\\Partition1\\yboxdash.xbe"],
        ["DASH1", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"],
        ["DASH2", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"],
        ["DASH3", "Device\\Harddisk0\\Partition1\\yboxdash.xbe"],
        ["FOG1CUSTOM", "a"],
        ["FOG1CUSTOM", "2"],
    ])
    def test_set_value_invalid(self, option, value):
        old_value = self.get(self.config, option)
        with self.assertRaises(ValueError):
            self.set(self.config, option, value)

        self.assertEquals(self.get(self.config, option), old_value)

    @parameterized.expand(itertools.product(os.listdir(TEST_CONFIG_DIR),
                                            sub_lists(IndBiosConfig().options(IndBiosConfig().get_default_section()))))
    def test_load_preset(self, preset_filename, apply_to_fields):
        apply_to_fields_in_section = {
            self.config.get_default_section(): apply_to_fields
        }
        values_before = dict(self.config.items(self.config.get_default_section()))
        preset_config = IndBiosConfig()
        self._read_config_for_obj(preset_config, preset_filename, True)
        self.config.load_preset(os.path.join(TEST_CONFIG_DIR, preset_filename), apply_to_fields_in_section)

        # Ideally I would I use subtest here so that if one assert fails the others will still be executed.
        # Unfortunately subtest is not available in Python 2. The other alternative would be to use parameterized to
        # perform a separate test for each field but that would be really slow.
        for field in self.config.options(self.config.get_default_section()):
            if field in apply_to_fields:
                self.assertEqual(self.get(self.config, field), self.get(preset_config, field))
            else:
                self.assertEqual(self.get(self.config, field), values_before[field])


if __name__ == '__main__':
    unittest.main()
