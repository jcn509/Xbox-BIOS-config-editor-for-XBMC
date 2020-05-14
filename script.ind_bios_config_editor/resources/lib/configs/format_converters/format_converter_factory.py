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
from .boolean_format_converter import BooleanFormatConverter
from .discrete_format_converter import DiscreteFormatConverter
from .dos_file_path_format_converter import DosFilePathFormatConverter
from .dos_file_path_or_zero_format_converter import DosFilePathOrZeroFormatConverter
from .integer_format_converter import IntegerFormatConverter
from .string_format_converter import StringFormatConverter

# There is no need for there to be more than 1 instance of these
_BOOLEAN_FORMAT_CONVERTER = BooleanFormatConverter()
_DOS_FILE_PATH_CONVERTER = DosFilePathFormatConverter()
_DOS_FILE_PATH_OR_ZERO_CONVERTER = DosFilePathOrZeroFormatConverter()
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
        return _DOS_FILE_PATH_OR_ZERO_CONVERTER
    elif isinstance(config_field, DVDFilePathField):
        return _DOS_FILE_PATH_CONVERTER
    else:
        FormatConverterFactoryError("Unrecognised type: " + str(type(config_field)))
