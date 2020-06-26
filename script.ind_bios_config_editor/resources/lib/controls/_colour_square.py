"""A helper control that displays a square with a given colour"""

import pyxbmct
import os
import xbmcaddon

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo("path")

_COLOUR_SQUARE_IMAGE_FILENAME = os.path.join(
    _addon_path, "resources", "media", "colour_picker_white_square.png"
)


class _ColourSquare(pyxbmct.Image):
    """A helper control that displays a square with a given colour"""

    def __new__(cls, color_diffuse):
        # parameter not used here. Not camel cae as that is not the convetion
        # used in PyXBMCt.
        return super(_ColourSquare, cls).__new__(
            cls, _COLOUR_SQUARE_IMAGE_FILENAME, aspectRatio=2
        )

    def __init__(self, color_diffuse):
        # type: (str) -> None
        # parameter not used here. Not camel cae as that is not the convetion
        # used in PyXBMCt.
        self.setColorDiffuse(color_diffuse)

    def setColorDiffuse(self, color_diffuse):
        """Override of the method from pyxbmct.Image
        
        :param colorDiffuse: a hex colour e.g. FFAA00, FFAAAABB, 0xFFFFFF
        """
        # type: (str) -> None
        if color_diffuse[0:2] == "0x":
            if len(color_diffuse) < 10:
                color_diffuse = color_diffuse[0:2] + "FF" + color_diffuse[2:]
        elif len(color_diffuse) < 8:
            color_diffuse = "FF" + color_diffuse
        super(_ColourSquare, self).setColorDiffuse(color_diffuse)
