"""Factory to produce format converter objects"""

try:
    # typing module not available on XBMC4XBOX
    from typing import Any, TYPE_CHECKING
    if TYPE_CHECKING:
        from ..format_converters import AbstractFormatConverter
except:
    pass

from ..config_field import (
    BooleanField,
    IntegerField,
    DiscreteField,
    StringField,
    HDDFilePathField,
    OptionalHDDFilePathField,
    DVDFilePathField,
    HexColourField,
)
from ..format_converters import (
    BooleanFormatConverter,
    DiscreteFormatConverter,
    DOSFilePathFormatConverter,
    IntegerFormatConverter,
    OptionalDOSFilePathFormatConverter,
    StringFormatConverter,
)

# There is no need for there to be more than 1 instance of these
_BOOLEAN_FORMAT_CONVERTER = BooleanFormatConverter()
_DOS_FILE_PATH_CONVERTER = DOSFilePathFormatConverter()
_OPTIONAL_DOS_FILE_PATH_CONVERTER = OptionalDOSFilePathFormatConverter()
_INTEGER_FORMAT_CONVERTER = IntegerFormatConverter()
_STRING_FORMAT_CONVERTER = StringFormatConverter()


class FormatConverterFactoryError(Exception):
    """Raised if there is some issue creating a format converter"""
    pass


def format_converter_factory(config_field):
    """Create a format converter for a field

    :param config_field: a config field description from :resoures.lib.configs.config_field:
    :returns: an object of a class from :resources.lib.format_converters:
    """
    # type: (Any) -> AbstractFormatConverter
    if isinstance(config_field, BooleanField):
        return _BOOLEAN_FORMAT_CONVERTER
    elif isinstance(config_field, IntegerField):
        return _INTEGER_FORMAT_CONVERTER
    elif isinstance(config_field, DiscreteField):
        return DiscreteFormatConverter(config_field.values)
    elif isinstance(config_field, (StringField, HexColourField)):
        return _STRING_FORMAT_CONVERTER
    elif isinstance(config_field, HDDFilePathField):
        return _DOS_FILE_PATH_CONVERTER
    elif isinstance(config_field, OptionalHDDFilePathField):
        return _OPTIONAL_DOS_FILE_PATH_CONVERTER
    elif isinstance(config_field, DVDFilePathField):
        return _DOS_FILE_PATH_CONVERTER
    else:
        raise FormatConverterFactoryError("Unrecognised type: " + str(type(config_field)))
