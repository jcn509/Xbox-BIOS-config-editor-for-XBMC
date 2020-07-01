"""Button with an icon and text"""
import os

try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable, Tuple, Union
except:
    pass

import pyxbmct
import xbmcaddon

from ..image_utils import get_png_aspect_ratio

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo("path")


class ButtonWithIcon(pyxbmct.Group):
    """Button with an icon and text"""

    def __new__(
        cls,
        text,
        icon_filename,
        icon_full_path=False,
        icon_scale = 68,
        set_icon_colour_diffuse_on_set_enabled=True,
        *args,
        **kwargs
    ):
        return super(ButtonWithIcon, cls).__new__(cls, 1, 2, *args, **kwargs)

    def __init__(
        self,
        text,
        icon,
        icon_full_path=False,
        icon_scale = 68,
        set_icon_colour_diffuse_on_set_enabled=True,
        *args,
        **kwargs
    ):
        """:param text: text label for the button
        :param icon: either an icon filename or a :pyxbmct.Image: ONLY PNG\
                IMAGES ARE SUPPORTED!
        :param icon_full_path: if False icon filename is seen as a relative\
                path from resources/media
        :param icon_scale: what percentage of the buttons width/height\
                (whichever gives the smaller value) should the icon take up
        :param set_icon_colour_diffuse_on_set_enabled: if True, when the\
                button is disabled the icon will become slightly transparent

        Note: operates under the assumption that:
            (icon_width / button_width) < (icon_height / button_height)
        """
        # type: (str, Union[str, pyxbmct.Image], bool, int, bool, Any, Any) -> None
        super(ButtonWithIcon, self).__init__(1, 2, *args, **kwargs)

        self._set_icon_colour_diffuse_on_set_enabled = (
            set_icon_colour_diffuse_on_set_enabled
        )

        if isinstance(icon, basestring):
            if not icon_full_path:
                icon = os.path.join(_addon_path, "resources", "media", icon)
            self._image_aspect_ratio = get_png_aspect_ratio(icon)
            self._icon = pyxbmct.Image(icon, aspectRatio=2)
        else:
            # Have no way of knowing what the true width and height of the
            # image is. Just guess that it is square...
            self._image_aspect_ratio = 1.0
            self._icon = icon  # type: pyxbmct.Image

        self._button = pyxbmct.Button(text)
        self._icon_scale = icon_scale

    def get_button(self):
        
        """:returns: the button component of the ButtonWithIcon"""
        # type: () -> pyxbmct.Button
        return self._button

    def get_icon(self):
        """:returns: the icon component of the ButtonWithIcon"""
        # type: () -> pyxbmct.Image
        return self._icon

    def setEnabled(self, enabled):
        """Overrides :pyxbmct.Group.setEnabled: (hence the camelcase)
        
        The icon becomes translucent when the button is disabled
        """
        # type: (bool) -> None
        self._button.setEnabled(enabled)

        if self._set_icon_colour_diffuse_on_set_enabled:
            if enabled:
                self._icon.setColorDiffuse("0xFFFFFFFF")
            else:
                self._icon.setColorDiffuse("0x5FFFFFFF")

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        # Connect the callback to the button instead
        # as that is what PyXBMCt will see being clicked
        window.connect(self._button, callback)
        return False



    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(ButtonWithIcon, self)._placedCallback(window, *args, **kwargs)

        self.placeControl(self._button, 0, 0, pad_x=0, pad_y=0, columnspan=2)

        # Previously I used placeControl but it made it very hard to line up
        # non-square images properly as the image object may have been larger
        # than the image itself. Therefore, it was difficult to know where the
        # edges of the actual image were... 
        self.addControl(self._icon)

        button_width = self._button.getWidth()
        button_height = self._button.getHeight()
        button_side = min(button_width, button_height)
        
        icon_height = button_height * (self._icon_scale / 100.0)
        icon_width = int(round(icon_height * self._image_aspect_ratio)) 
        icon_height = int(icon_height)

        self._icon.setWidth(icon_width)
        self._icon.setHeight(icon_height)
        
        button_x, button_y = self._button.getPosition()
        
        padding = (button_height - icon_height) / 2
        icon_x = button_x + button_width - (icon_width + padding)
        icon_y = button_y + padding
        self._icon.setPosition(icon_x, icon_y)



