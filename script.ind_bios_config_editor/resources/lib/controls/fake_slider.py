try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass
import pyxbmct
import xbmcgui
import os
from .abstract_control import AbstractControl


class FakeSlider(AbstractControl, pyxbmct.Group):
    """Implements a movable slider for adjusting some value.

    Not a derivate of ControlSlider class.
    """

    def __new__(
        cls,
        min_value=0,
        max_value=255,
        default_value=None,
        step=1,
        click_to_type_value=True,
        keyboard_title="Enter Number",
        show_value_label=True,
        value_label_width=1,
        total_width=4,
        outline_texture=None,
        nib_texture_not_focussed=None,
        nib_texture_focussed=None,
        *args,
        **kwargs
    ):
        return super(FakeSlider, cls).__new__(cls, 1, 1, *args, **kwargs)

    def __init__(
        self,
        min_value=0,
        max_value=255,
        default_value=None,
        step=1,
        click_to_type_value=True,
        keyboard_title="Enter Number",
        show_value_label=True,
        value_label_width=1,
        total_width=4,
        outline_texture=None,
        nib_texture_not_focussed=None,
        nib_texture_focussed=None,
        *args,
        **kwargs
    ):
        """:param step: how much the value changes with each movement of the\
                slider
        :param click_to_type_value: if True, when the user clicks on the\
                slider a keyboard pops up that they can use to type in a\
                number
        :param keyboard_title: the title that will be displayed on the\
                keyboard window
        :param show_value_label: show a label next to the slider that\
                displays the current value
        :param value_label_width: the number of columns that the value label\
                takes up
        :param total_width: the total number of columns in the grid
        :param outline_texture: the outline texture image filename
        :param nib_texture_not_focussed: the texture of the slider nib when\
                the slider is not in focus
        :param nib_texture_focussed: the texture of the slider nib when the\
                slider is in focus
        """
        # type: (int, int, int, int, bool, str, bool, int, int, str, str, str, Any, Any) -> None
        super(FakeSlider, self).__init__(1, total_width, *args, **kwargs)

        if max_value < min_value:
            raise ValueError("max_value must be >= min_value")
        if default_value == None:
            default_value = min_value
        if default_value > max_value:
            raise ValueError("default_value must be <= max_value")
        if default_value < min_value:
            raise ValueError("default_value must be >= min_value")

        self._outline_texture = (
            outline_texture
            if outline_texture
            else os.path.join(pyxbmct.skin.images, "Slider", "osd_slider_bg.png")
        )
        self._nib_texture_not_focussed = (
            nib_texture_not_focussed
            if nib_texture_not_focussed
            else os.path.join(pyxbmct.skin.images, "Slider", "osd_slider_nibNF.png")
        )
        self._nib_texture_focussed = (
            nib_texture_focussed
            if nib_texture_focussed
            else os.path.join(pyxbmct.skin.images, "Slider", "osd_slider_nib.png")
        )

        # if xbmc.getInfoLabel('System.BuildVersion')[:2] >= '17':
        #    kwargs['orientation'] = xbmcgui.HORIZONTAL

        self._value_changed_callback = None
        self._step = step
        self._min_value = min_value
        self._max_value = max_value
        self._default_value = default_value

        self._keyboard_title = keyboard_title
        self._click_to_type_value = click_to_type_value

        self._show_value_label = show_value_label
        self._value_label_width = value_label_width
        self._total_width = total_width

    def get_value(self):
        """:returns: the current value of the slider"""
        # type: () -> int
        return self._value

    def _add_to_value_if_focussed(self, num_to_add):
        # type: (int) -> None
        if self._window.getFocus() == self._nib:
            self.set_value(self._value + num_to_add)

    def _increase_if_focussed(self):
        """Increase current value by the step value if the slider is in focus"""
        # type: () -> None
        self._add_to_value_if_focussed(self._step)

    def _decrease_if_focussed(self):
        """Decrease the slider by the step value of it the slider is in focus"""
        # type: () -> None
        self._add_to_value_if_focussed(-self._step)

    def set_value(self, value, trigger_callback=True):
        """Set the value of the slider
        :param trigger_callback: if False the whatever callback is connected\
                to the slider won't be called
        """
        # type: (int, bool) -> None
        if value < self._min_value:
            value = self._min_value
        elif value > self._max_value:
            value = self._max_value

        self._value = value
        nib_x = int(
            round(self._nib_min_x + (float(value - self._min_value) * self._nib_x_unit))
        )

        self._nib.setPosition(nib_x, self._nib_y)

        if self._show_value_label:
            self._value_label.setLabel(str(value))

        if trigger_callback and self._value_changed_callback:
            self._value_changed_callback(value)

    def _type_value(self):
        """Open a keyboard to allow the user to type in a value instead of\
                using the slider
        """
        # type: () -> None
        dialog = xbmcgui.Dialog()
        self.set_value(
            int(dialog.numeric(0, self._keyboard_title, str(self.get_value())))
        )

        # I believe these aren't garbage collected?
        del dialog

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._value_changed_callback = callback
        return False # Don't use PyXBMCt's built in callback mechanism

    def _placedCallback(self, window, *args, **kwargs):
        super(FakeSlider, self)._placedCallback(window, *args, **kwargs)

        if self._show_value_label:
            slider_width = self._total_width - self._value_label_width
            label_text_align = pyxbmct.ALIGN_CENTER_Y
            self._value_label = pyxbmct.Label("", alignment=label_text_align)
            label_column = self._total_width - self._value_label_width
            self.placeControl(
                self._value_label,
                0,
                label_column,
                columnspan=self._value_label_width,
                pad_x=10,
                pad_y=0,
            )
        else:
            slider_width = self._total_width

        self._window = window
        width = int(
            round(
                float(self.getWidth())
                * (float(slider_width) / float(self._total_width))
            )
        )
        height = self.getHeight()
        x, y = self.getPosition()

        nib_pad = 0
        nib_size = min(width, height) - (2 * nib_pad)

        self._nib_min_x = float(x)  # Need a float later
        self._nib_y = y + (height / 2) - (nib_size / 2)
        self._nib_x_unit = float(width - nib_size) / float(
            self._max_value - self._min_value
        )

        self._nib = pyxbmct.Button(
            "",
            focusTexture=self._nib_texture_not_focussed,
            noFocusTexture=self._nib_texture_focussed,
        )
        self._nib.setWidth(nib_size)
        self._nib.setHeight(nib_size)

        # This is a bodge to ensure that window.autoNavigation works
        # properly for controls above or below the slider.
        # nib should never be accessed from the outside anyway...
        self._nib.getWidth = lambda: width
        self._nib.getHeight = lambda: height
        self._nib.getPosition = lambda: (x, y)

        self.addControl(self._nib)

        self.set_value(self._default_value, False)

        if self._click_to_type_value:
            window.connect(self._nib, self._type_value)

        # Stop window.autoNavigation from allowing one to move
        # From this control to one on the left or right
        self._nib.controlLeft = lambda x: None
        self._nib.controlRight = lambda x: None
        window.connectEventList(
            [pyxbmct.ACTION_MOVE_RIGHT, pyxbmct.ACTION_MOUSE_WHEEL_UP],
            self._increase_if_focussed,
        )
        window.connectEventList(
            [pyxbmct.ACTION_MOVE_LEFT, pyxbmct.ACTION_MOUSE_WHEEL_DOWN],
            self._decrease_if_focussed,
        )

        outline = pyxbmct.Image(self._outline_texture)
        self.placeControl(outline, 0, 0, columnspan=slider_width, pad_x=0, pad_y=0)

    def _removedCallback(self, window):
        window.disconnectEventList(
            [pyxbmct.ACTION_MOVE_RIGHT, pyxbmct.ACTION_MOUSE_WHEEL_UP],
            self._increase_if_focussed,
        )
        window.disconnectEventList(
            [pyxbmct.ACTION_MOVE_LEFT, pyxbmct.ACTION_MOUSE_WHEEL_DOWN],
            self._decrease_if_focussed,
        )
