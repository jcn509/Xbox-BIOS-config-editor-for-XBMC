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
from ..validators import (
    BooleanValidator,
    IntegerValidator,
    DiscreteValidator,
    RegexMatchPatternValidator,
    ColourWithAlphaValidator,
    ColourValidator,
    DVDFilePathValidator,
    HDDFilePathValidator,
    OptionalHDDFilePathValidator,
)

_BOOLEAN_VALIDATOR = BooleanValidator()
_COLOUR_VALIDATOR = ColourValidator()
_COLOUR_WITH_ALPHA_VALIDATOR = ColourWithAlphaValidator()


class ValidatorFactoryError(Exception):
    pass


def validator_factory(config_field):
    if isinstance(config_field, BooleanField):
        return _BOOLEAN_VALIDATOR
    elif isinstance(config_field, IntegerField):
        return IntegerValidator(config_field.min_value, config_field.max_value)
    elif isinstance(config_field, DiscreteField):
        return DiscreteValidator(config_field.values)
    elif isinstance(config_field, StringField):
        return RegexMatchPatternValidator(config_field.regex)
    elif isinstance(config_field, HDDFilePathField):
        return HDDFilePathValidator(config_field.file_extension)
    elif isinstance(config_field, OptionalHDDFilePathField):
        return OptionalHDDFilePathValidator(config_field.file_extension)
    elif isinstance(config_field, DVDFilePathField):
        return DVDFilePathValidator(config_field.file_extension)
    elif isinstance(config_field, HexColourField):
        return (
            _COLOUR_WITH_ALPHA_VALIDATOR
            if config_field.with_alpha_channel
            else _COLOUR_VALIDATOR
        )
    else:
        raise ValidatorFactoryError("Unrecognised type: " + str(type(config_field)))
