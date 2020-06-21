"""Factory to create validator objects"""

try:
    # typing module not available on XBMC4XBOX
    from typing import Any, TYPE_CHECKING
    if TYPE_CHECKING:
        from ..validators import AbstractValidator
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
from ..validators import (
    BooleanValidator,
    IntegerValidator,
    DiscreteValidator,
    RegexPatternMatchValidator,
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
    """Raised if there is an issue creating a validator"""
    pass


def validator_factory(config_field):
    """Create the appropriate validator for config_field"""
    # type: (Any) ->  AbstractValidator
    if isinstance(config_field, BooleanField):
        return _BOOLEAN_VALIDATOR
    elif isinstance(config_field, IntegerField):
        return IntegerValidator(config_field.min_value, config_field.max_value)
    elif isinstance(config_field, DiscreteField):
        return DiscreteValidator(config_field.values)
    elif isinstance(config_field, StringField):
        return RegexPatternMatchValidator(config_field.regex)
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
