"""Validate hexadecimal colours (with or without an alpha channel)"""
from .regex_pattern_match_validator import RegexPatternMatchValidator


class _HexValidator(RegexPatternMatchValidator):
    """Used to validate values of the form 0x followed by some number of
    alphanumeric characters
    """

    def __init__(self, length):
        # type: (int) -> None
        super(_HexValidator, self).__init__("^0x[0-9a-fA-F]{" + str(length) + "}$")


class ColourValidator(_HexValidator):
    """Validate colours without an alpha channel e.g. 0XFFAA00"""

    def __init__(self):
        super(ColourValidator, self).__init__(6)


class ColourWithAlphaValidator(_HexValidator):
    """Validate colours with an alpha channel e.g. 0XFFAA00BB"""

    def __init__(self):
        super(ColourWithAlphaValidator, self).__init__(8)
