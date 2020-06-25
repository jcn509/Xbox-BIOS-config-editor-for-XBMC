try:
    # typing is not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass
import pyxbmct
from .fake_slider import FakeSlider
from ._colour_square import _ColourSquare
from .abstract_control import AbstractControl


class ColourPickerFull(AbstractControl, pyxbmct.Group):
    """Full colour picker control with sliders and colour display"""

    def __new__(
        cls, alpha_selector=False, default_colour="0xFFFFFFFF", *args, **kwargs
    ):
        return super(ColourPickerFull, cls).__new__(cls, 1, 2, *args, **kwargs)

    def __init__(
        self, alpha_selector=False, default_colour="0xFFFFFFFF", *args, **kwargs
    ):
        """:param alpha_selector: if True then you can also pick the colour's\
                alpha component
        :param default_colour: a hexadecimal colour string optionally\
                prefixed with 0x. If alpha_selector is True then the first 2\
                characters represent the alpha channel
        """
        # type: (bool, str, Any, Any) -> None
        self._current_colour = default_colour

        num_rows = 3

        if alpha_selector:
            num_rows += 1
        else:
            if default_colour[0:2] == "0x":
                if len(default_colour) == 10:
                    default_colour = default_colour[0:2] + default_colour[4:]
            elif len(default_colour) == 8:
                default_colour = default_colour[2:]
        super(ColourPickerFull, self).__init__(num_rows, 7, *args, **kwargs)

        self._num_rows = num_rows
        self._alpha_selector = alpha_selector

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._colour_changed_callback = callback
        return False  # Don't use PyXBMCt's inbuilt connect mechanism

    def _placedCallback(self, window, *args, **kwargs):
        super(ColourPickerFull, self)._placedCallback(window, *args, **kwargs)

        self._colour_square = _ColourSquare(self._current_colour)
        self.placeControl(
            self._colour_square, 0, 5, rowspan=self._num_rows, columnspan=2
        )

        button_labels = ["Red", "Green", "Blue"]
        if self._alpha_selector:
            button_labels.insert(0, "Alpha")
        modify_colour_position = 2 if self._current_colour[0:2] == "0x" else 0

        for i, label_text in enumerate(button_labels):
            label_control = pyxbmct.Label(label_text)
            self.placeControl(label_control, i, 0)
            initial_value = int(
                self._current_colour[
                    modify_colour_position : modify_colour_position + 2
                ],
                16,
            )
            callback = lambda value, pos=modify_colour_position: self._modify_colour(
                pos, value
            )
            slider = FakeSlider(default_value=initial_value, keyboard_title=label_text)
            window.connect(slider, callback)
            self.placeControl(slider, i, 1, columnspan=4, pad_y=10)
            modify_colour_position += 2

    def set_value(self, colour, trigger_callback=True):
        """:param colour: is a hexadecimal colour string\
                e.g. 0xFFFFFF or 000000 or FFFFFFFF if you have an alpha\
                channel
        :param trigger_callback: if False then the colour chosen callback\
                will not be triggered
        """
        # type (str, bool) -> None
        self._current_colour = colour
        self._colour_square.setColorDiffuse(self._current_colour)

        if trigger_callback and self._colour_changed_callback:
            self._colour_changed_callback(colour)

    def get_value(self):
        """:returns: a hexadecimal colour string\
                e.g. 0xFFFFFF or 000000 or FFFFFFFF if you have an alpha\
                channel
        """
        # type: () -> str
        return self._current_colour

    def _modify_colour(self, position, value):
        """Modify the current colour, change the 2 characters at the given
        position

        Used to change e.g. the red component of the colour
        """
        colour = (
            self._current_colour[:position]
            + "{:02X}".format(value)
            + self._current_colour[position + 2 :]
        )
        self.set_value(colour)
