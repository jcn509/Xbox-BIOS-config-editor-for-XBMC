"""A helper control that displays a square with a given colour"""

import pyxbmct
import os
import xbmcaddon

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo("path")


class _ColourSquare(pyxbmct.Image):
    """A helper control that displays a square with a given colour"""

    def __new__(cls, colorDiffuse):
        # parameter not used here. Not camel cae as that is not the convetion
        # used in PyXBMCt.
        image_file = os.path.join(
            _addon_path, "resources", "media", "colour_picker_white_square.png"
        )
        return super(_ColourSquare, cls).__new__(cls, image_file, aspectRatio=2)

    def __init__(self, colorDiffuse):
        # type: (str) -> None
        # parameter not used here. Not camel cae as that is not the convetion
        # used in PyXBMCt.
        self.setColorDiffuse(colorDiffuse)

    def setColorDiffuse(self, colorDiffuse):
        """Override of the method from pyxbmct.Image
        
        :param colorDiffuse: a hex colour e.g. FFAA00, FFAAAABB, 0xFFFFFF
        """
        # type: (str) -> None
        if colorDiffuse[0:2] == "0x":
            if len(colorDiffuse) < 10:
                colorDiffuse = colorDiffuse[0:2] + "FF" + colorDiffuse[2:]
        elif len(colorDiffuse) < 8:
            colorDiffuse = "FF" + colorDiffuse
        super(_ColourSquare, self).setColorDiffuse(colorDiffuse)
