import pyxbmct
from .. import controls


class ColourPicker(pyxbmct.AddonDialogWindow):
    def __new__(
        cls,
        window_title="Choose Colour",
        alpha_selector=False,
        current_colour="0xFFFFFFFF",
        colour_chosen_callback=None,
    ):
        return super(ColourPicker, cls).__new__(cls)

    def __init__(
        self,
        window_title="Choose Colour",
        alpha_selector=False,
        current_colour="0xFFFFFFFF",
        colour_chosen_callback=None,
    ):
        super(ColourPicker, self).__init__(window_title)

        num_rows = 5 if alpha_selector else 4
        height = 60 * num_rows
        self.setGeometry(500, height, num_rows, 5)

        self._current_colour = current_colour
        self._colour_chosen_callback = colour_chosen_callback

        ok_button = controls.ButtonWithIcon("OK", "done.png")
        cancel_button = controls.ButtonWithIcon("Cancel", "close.png")
        colour_picker_full = controls.ColourPickerFull(alpha_selector, current_colour)
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
        self._current_colour = colour

    def _ok_button_pressed(self):
        if self._colour_chosen_callback:
            self._colour_chosen_callback(self._current_colour)
        self.close()
