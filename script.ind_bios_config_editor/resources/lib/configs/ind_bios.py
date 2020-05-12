from .abstract_config import AbstractConfig
from .ind_bios_fields import IND_BIOS_FIELDS


class IndBiosConfig(AbstractConfig):
    def __init__(self, *args, **kwargs):
        super(IndBiosConfig, self).__init__(*args, max_line_length=300, quote_char_if_whitespace='"', **kwargs)

    def _get_fields(self):
        return IND_BIOS_FIELDS

    def _get_true_if_non_default(self):
        return {
            "FOG1CUSTOM": ["FOG1COLOR"],
            "FOG2CUSTOM": ["FOG2COLOR"]
        }

    def _get_true_if_non_zero(self):
        return {
            "SKEWEN": ["XSKEWLOGO", "YSKEWLOGO"]
        }
