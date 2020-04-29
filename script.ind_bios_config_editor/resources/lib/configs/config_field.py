from collections import namedtuple

_CONFIG_FIELDS = ('field_name', 'default_value',)

BooleanField = namedtuple("BooleanField", _CONFIG_FIELDS)
IntegerField = namedtuple("IntegerField", _CONFIG_FIELDS + ("min_value", "max_value"))
DiscreteField = namedtuple("BooleanField", _CONFIG_FIELDS + ("values", ))
StringField = namedtuple("ConfigField", _CONFIG_FIELDS + ("regex", ))

_FILE_PATH_DEVICES = namedtuple("FilePathDevices", ("HDD", "DVD"))("Harddisk0\\\\Partition[1267]", "CdRom0")
_FILE_PATH_FIELDS = _CONFIG_FIELDS + ("file_extension", )
HDDFilePathField = namedtuple("HDDFilePathField", _FILE_PATH_FIELDS)
OptionalHDDFilePathField = namedtuple("OptionalHDDFilePathField", _FILE_PATH_FIELDS)
DVDFilePathField = namedtuple("DVDFilePathField", _FILE_PATH_FIELDS)

HexColourField = namedtuple("HexColourField", _CONFIG_FIELDS + ("with_alpha_channel",))

