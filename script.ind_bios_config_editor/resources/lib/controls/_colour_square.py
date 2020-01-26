import pyxbmct
import os
import xbmcaddon

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')

class _ColourSquare(pyxbmct.Image):
    # Used camelCase for parameter as that is what is done in pyxbmct
    def __new__(cls, colorDiffuse):
        image_file = os.path.join(_addon_path, 'resources', 'media', 'colour_picker_white_square.png')
        return super(_ColourSquare, cls).__new__(cls, image_file, aspectRatio=2)

    def __init__(self, colorDiffuse):
        self.setColorDiffuse(colorDiffuse)

    def setColorDiffuse(self, colorDiffuse):
        if colorDiffuse[0:2] == "0x":
            if len(colorDiffuse) < 10:
                colorDiffuse = colorDiffuse[0:2] + "FF" + colorDiffuse[2:]
        elif len(colorDiffuse) < 8:
            colorDiffuse = "FF" + colorDiffuse
        super(_ColourSquare, self).setColorDiffuse(colorDiffuse)
