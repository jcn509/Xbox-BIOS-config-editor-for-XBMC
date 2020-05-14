import pyxbmct
import xbmcaddon
import os

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo("path")


class ButtonWithIcon(pyxbmct.Group):
    def __new__(
        cls,
        text,
        icon_filename,
        icon_full_path=False,
        icon_pad_x=5,
        icon_pad_y=5,
        *args,
        **kwargs
    ):
        return super(ButtonWithIcon, cls).__new__(cls, 1, 2, *args, **kwargs)

    def __init__(
        self,
        text,
        icon_filename,
        icon_full_path=False,
        icon_pad_x=5,
        icon_pad_y=5,
        *args,
        **kwargs
    ):
        super(ButtonWithIcon, self).__init__(1, 2, *args, **kwargs)
        if not icon_full_path:
            icon_filename = os.path.join(
                _addon_path, "resources", "media", icon_filename
            )

        self._button = pyxbmct.Button(text)
        self._icon = pyxbmct.Image(icon_filename, aspectRatio=2)
        self._icon_pad_x = icon_pad_x
        self._icon_pad_y = icon_pad_y

    def get_button(self):
        return self._button

    def get_icon(self):
        return self._icon

    def _icon_placed(self, window, row, column, rowspan, columnspan, pad_x, pad_y):
        icon_x, icon_y = self._icon.getPosition()
        icon_width = self._icon.getWidth()
        # Using the min of getWidth and getHeight as the image is square and
        # this gives the width of the actual image, rather than the width of the
        # image object which may be very wide
        icon_side = min(icon_width, self._icon.getHeight())

        button_x, button_y = self._button.getPosition()
        button_width = self._button.getWidth()

        new_icon_x = button_x + button_width - ((icon_side + icon_width) / 2 + pad_x)
        self._icon.setPosition(new_icon_x, icon_y)

    def setEnabled(self, enabled):
        self._button.setEnabled(enabled)
        if enabled:
            self._icon.setColorDiffuse("0xFFFFFFFF")
        else:
            self._icon.setColorDiffuse("0x5FFFFFFF")

    def _connectCallback(self, callable, window):
        window.connect(self._button, callable)
        return False

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(ButtonWithIcon, self)._placedCallback(window, *args, **kwargs)

        self.placeControl(self._button, 0, 0, pad_x=0, pad_y=0, columnspan=2)

        self._icon._placedCallback = self._icon_placed
        self.placeControl(
            self._icon, 0, 1, pad_x=self._icon_pad_x, pad_y=self._icon_pad_y
        )
