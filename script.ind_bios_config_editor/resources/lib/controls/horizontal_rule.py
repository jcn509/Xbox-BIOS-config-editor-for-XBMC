import pyxbmct
import xbmcaddon
import os

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo("path")


class HorizontalRule(pyxbmct.Image):
    def __new__(cls):
        image_file = os.path.join(
            _addon_path, "resources", "media", "horizontal_rule.png"
        )
        return super(HorizontalRule, cls).__new__(cls, image_file)

    def __init__(self):
        super(HorizontalRule, self).setColorDiffuse("0x00000000")
