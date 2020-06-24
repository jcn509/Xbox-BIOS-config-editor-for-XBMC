"""Represents the iND-BiOS config file"""

try:
    # typing not available on XBMC4XBOX
    from typing import Dict, Any
except:
    pass

from .abstract_config import AbstractConfig
from .ind_bios_fields import IND_BIOS_FIELDS


class IndBiosConfig(AbstractConfig):
    """Read and edit the iND-BiOS config"""
    def __init__(self, *args, **kwargs):
        super(IndBiosConfig, self).__init__(
            *args, max_line_length=300, quote_char_if_whitespace='"', **kwargs
        )

    def _get_fields(self):
        """:returns: a tuple describing all the fields in the iND-BiOS"""
        return IND_BIOS_FIELDS
    
    def _get_true_if_fields_dont_have_values(self):
        """:returns: values to set to True if other values have certain\
                values(or False otherwise)
        """
        # type: () -> Dict[str, Dict[str, Any]]
        return {
            "FOG1CUSTOM" : {
                "FOG1COLOR": IND_BIOS_FIELDS.fog1color.default_value
            },
            "FOG1CUSTOM": {
                "FOG2COLOR": IND_BIOS_FIELDS.fog2color.default_value
            },
            "SKEWEN": {
                "XSKEWLOGO": 0,
                "YSKEWLOGO": 0
            }
        }
