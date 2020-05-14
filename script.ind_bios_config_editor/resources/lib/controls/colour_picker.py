import pyxbmct
import xbmc
from .fake_slider import FakeSlider
from ._colour_square import _ColourSquare
from .colour_picker_full import ColourPickerFull
from .abstract_control import AbstractControl


class ColourPicker(AbstractControl, pyxbmct.Group):
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
        super(ColourPicker, self).__init__(1, 2, *args, **kwargs)

        if not alpha_selector:
            if default_colour[0:2] == "0x":
                if len(default_colour) == 10:
                    default_colour = default_colour[0:2] + default_colour[4:]
            else:
                if len(default_colour) == 8:
                    default_colour = default_colour[2:]

        self._current_colour = default_colour
        self._window_title = window_title
        self._alpha_selector = alpha_selector
        self._colour_chosen_callback = None

    def set_value(self, colour, trigger_callback=True):
        self._current_colour = colour
        self._button.setLabel(colour)
        self._colour_square.setColorDiffuse(colour)
        if trigger_callback and self._colour_chosen_callback:
            self._colour_chosen_callback(colour)

    def get_value(self):
        return self._current_colour

    def pick_colour(self):
        # Windows also imports Controls. To avoid circular import issues the
        # importing of windows is delayed until now.
        from .. import windows

        colour_picker = windows.ColourPicker(
            self._window_title,
            self._alpha_selector,
            self._current_colour,
            self.set_value,
        )
        colour_picker.doModal()
        # Destroy the instance explicitly because
        # underlying xbmcgui classes are not garbage-collected on exit.
        del colour_picker

    def _colour_square_placed(
        self, window, row, column, rowspan, columnspan, pad_x, pad_y
    ):
        square_x, square_y = self._colour_square.getPosition()
        square_width = self._colour_square.getWidth()
        # Using the min of getWidth and getHeight as the image is square and
        # this gives the width of the actual image, rather than the width of the
        # image object which may be very wide
        square_side = min(
            self._colour_square.getWidth(), self._colour_square.getHeight()
        )

        button_x, button_y = self._button.getPosition()
        button_width = self._button.getWidth()

        new_square_x = (
            button_x + button_width - ((square_side + square_width) / 2 + pad_x)
        )
        self._colour_square.setPosition(new_square_x, square_y)

    def _connectCallback(self, callable, window):
        self._colour_chosen_callback = callable
        return False

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(ColourPicker, self)._placedCallback(window, *args, **kwargs)
        self._button = pyxbmct.Button(self._current_colour)
        self.placeControl(self._button, 0, 0, columnspan=2, pad_x=0, pad_y=0)

        self._colour_square = _ColourSquare(self._current_colour)
        self._colour_square._placedCallback = self._colour_square_placed
        self.placeControl(self._colour_square, 0, 1)

        # Need to temporarily disable _connectCallback so that ithas no effect
        # when window.connect is called below
        temp = self._connectCallback
        self._connectCallback = lambda x, y: True
        window.connect(self._button, self.pick_colour)
        self._connectCallback = temp

        self.set_value(self._current_colour, False)
