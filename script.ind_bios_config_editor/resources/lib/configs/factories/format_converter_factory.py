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
    DosFilePathFormatConverter,
    IntegerFormatConverter,
    OptionalDosFilePathFormatConverter,
    StringFormatConverter,
)

# There is no need for there to be more than 1 instance of these
_BOOLEAN_FORMAT_CONVERTER = BooleanFormatConverter()
_DOS_FILE_PATH_CONVERTER = DosFilePathFormatConverter()
_OPTIONAL_DOS_FILE_PATH_CONVERTER = OptionalDosFilePathFormatConverter()
_INTEGER_FORMAT_CONVERTER = IntegerFormatConverter()
_STRING_FORMAT_CONVERTER = StringFormatConverter()


class FormatConverterFactoryError(Exception):
    pass


def format_converter_factory(config_field):
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
        FormatConverterFactoryError("Unrecognised type: " + str(type(config_field)))
