"""Colour pickers"""

try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass
import pyxbmct
import xbmc

from .abstract_control import AbstractControl
from .button_with_icon import ButtonWithIcon
from ._colour_square import _ColourSquare
from .colour_picker_full import ColourPickerFull
from .fake_slider import FakeSlider

# Note: this window is here and not in the Windows package as:
# a) it only really needs to be used with this control
# b) it lead to circular imports which pytype couldn't handle
# c) it makes it easier to re-use this contol as now you only need the
#    controls package
class _ColourPickerWindow(pyxbmct.AddonDialogWindow):
    """Contains controls used to pick a colour"""

    def __new__(
        cls,
        window_title="Choose Colour",
        alpha_selector=False,
        current_colour="0xFFFFFFFF",
        colour_chosen_callback=None,
    ):
        return super(_ColourPickerWindow, cls).__new__(cls)

    def __init__(
        self,
        window_title="Choose Colour",
        alpha_selector=False,
        current_colour="0xFFFFFFFF",
        colour_chosen_callback=None,
    ):
        """:param alpha_selector: if True then you can also pick the colour's\
                alpha component
        :param current_colour: a hexadecimal colour string optionally\
                prefixed with 0x. If alpha_selector is True then the first 2\
                characters represent the alpha channel
        """

        # type: (str, bool, str, Callable) -> None
        super(_ColourPickerWindow, self).__init__(window_title)

        num_rows = 5 if alpha_selector else 4
        height = 60 * num_rows
        self.setGeometry(500, height, num_rows, 5)

        self._current_colour = current_colour
        self._colour_chosen_callback = colour_chosen_callback

        ok_button = ButtonWithIcon("OK", "done.png")
        cancel_button = ButtonWithIcon("Cancel", "close.png")
        colour_picker_full = ColourPickerFull(alpha_selector, current_colour)
        self.placeControl(colour_picker_full, 0, 0, columnspan=5, rowspan=num_rows - 1)
        self.placeControl(ok_button, num_rows - 1, 0, columnspan=2)
        self.placeControl(cancel_button, num_rows - 1, 3, columnspan=2)

        self.autoNavigation()

        self.connect(ok_button, self._ok_button_pressed)
        self.connect(cancel_button, self.close)
        self.connect(colour_picker_full, self._colour_changed)
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.setFocus(ok_button)

    def _colour_changed(self, colour):
        # type: (str) -> None
        self._current_colour = colour

    def _ok_button_pressed(self):
        # type: () -> None
        if self._colour_chosen_callback:
            self._colour_chosen_callback(self._current_colour)
        self.close()


class ColourPicker(AbstractControl, ButtonWithIcon):
    """Colour picker button that displays the Current colour and opens a
    colour picker window when clicked
    """

    def __new__(
        cls,
        window_title="Choose Colour",
        alpha_selector=False,
        default_colour="0xFFFFFFFF",
        *args,
        **kwargs
    ):
        return super(ColourPicker, cls).__new__(cls, 1, 2, *args, **kwargs)

    def __init__(
        self,
        window_title="Choose Colour",
        alpha_selector=False,
        default_colour="0xFFFFFFFF",
        *args,
        **kwargs
    ):
        """:param alpha_selector: if True then you can also pick the colour's\
                alpha component
        :param default_colour: a hexadecimal colour string optionally\
                prefixed with 0x. If alpha_selector is True then the first 2\
                characters represent the alpha channel
        """
        # type: (str, bool, str, Any, Any) -> None
        
        self._alpha_selector = alpha_selector
        self._current_colour = self._get_colour_in_correct_format(default_colour)
        
        colour_square = _ColourSquare(self._current_colour)
        super(ColourPicker, self).__init__(self._current_colour, colour_square, *args, **kwargs)

        self._window_title = window_title
        self._colour_chosen_callback = None
    
    def _get_colour_in_correct_format(self, colour):
        """Cut out alpha component if it shouldn't be there"""
        # type: (str) -> str
        if not self._alpha_selector:
            if colour[0:2] == "0x":
                if len(colour) == 10:
                    colour = colour[0:2] + colour[4:]
            else:
                if len(colour) == 8:
                    colour = colour[2:]
        
        return colour


    def set_value(self, colour, trigger_callback=True):
        """:param colour: is a hexadecimal colour string\
                e.g. 0xFFFFFF or 000000 or FFFFFFFF if you have an alpha\
                channel
        :param trigger_callback: if False then the colour chosen callback\
                will not be triggered
        """
        # type (str, bool) -> None
        colour = self._get_colour_in_correct_format(colour)
        self._current_colour = colour
        
        self._button.setLabel(colour)
        self._icon.setColorDiffuse(colour)
        
        if trigger_callback and self._colour_chosen_callback is not None:
            self._colour_chosen_callback(colour)

    def get_value(self):
        """:returns: a hexadecimal colour string\
                e.g. 0xFFFFFF or 000000 or FFFFFFFF if you have an alpha\
                channel
        """
        # type: () -> str
        return self._current_colour

    def pick_colour(self):
        """Open the colour picker window so you can pick a new colour"""
        # type: () -> None
        colour_picker = _ColourPickerWindow(
            self._window_title,
            self._alpha_selector,
            self._current_colour,
            self.set_value,
        )
        colour_picker.doModal()
        # Destroy the instance explicitly because
        # underlying xbmcgui classes are not garbage-collected on exit.
        del colour_picker

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) ->  bool
        self._colour_chosen_callback = callback
        return False  # Don't use PyXBMCt's default connection mechanism

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(ColourPicker, self)._placedCallback(window, *args, **kwargs)

        # Need to temporarily disable _connectCallback so that it has no effect
        # when window.connect is called below
        temp = self._connectCallback
        self._connectCallback = lambda x, y: True
        window.connect(self, self.pick_colour)
        self._connectCallback = temp
