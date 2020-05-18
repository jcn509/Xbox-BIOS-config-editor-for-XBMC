from .regex_pattern_match_validator import RegexPatternMatchValidator


class HexValidator(RegexPatternMatchValidator):
    def __init__(self, length):
        super(HexValidator, self).__init__("^0x[0-9a-fA-F]{" + str(length) + "}$")


class ColourValidator(HexValidator):
    def __init__(self):
        super(ColourValidator, self).__init__(6)


class ColourWithAlphaValidator(HexValidator):
    def __init__(self):
        super(ColourWithAlphaValidator, self).__init__(8)
