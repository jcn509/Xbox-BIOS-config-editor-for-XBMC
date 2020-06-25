"""Used to select the Xbox's front panel LED pattern"""

try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass

import pyxbmct
import xbmcaddon

from .abstract_control import AbstractControl


class LedPattern(AbstractControl, pyxbmct.Group):
    """Used to select the Xbox's front panel LED pattern
    
    The pattern is represented as a 4 character string. Each character
    represents one stage of the pattern. iND-BiOS cycles through each stage
    of the pattern in turn

    Valid values for each character are:
    - G (Green)
    - R (Off)
    - O (Orange)
    - O (Off)

    The values for each character are chosen by using a red and green radio
    button. If both radio buttons are on orange is selected, if both are off
    off is selected, and if only one is on that colour is selected.
    """

    def __new__(
        cls,
        label_text="LED pattern (green + red = orange, neither = off)",
        default_pattern="GGGG",
        *args,
        **kwargs
    ):
        return super(LedPattern, cls).__new__(cls, 5, 3, *args, **kwargs)

    def __init__(
        self,
        label_text="LED pattern (green + red = orange, neither = off)",
        default_pattern="GGGG",
        *args,
        **kwargs
    ):
        # type: (str, str, Any, Any) -> None
        super(LedPattern, self).__init__(5, 3, *args, **kwargs)
        self._pattern = default_pattern
        self._label_text = label_text

    def _change_pattern_position(self, position):
        """Change a character at the given position

        Character to use comes from the values of the red and green radio
        buttons at that position
        """
        # type: (int) -> None
        green = self._green_radio_buttons[position].isSelected()
        red = self._red_radio_buttons[position].isSelected()
        colour_char = "B"  # LED off
        if green and red:
            colour_char = "O"
        elif green:
            colour_char = "G"
        elif red:
            colour_char = "R"

        self._pattern = (
            self._pattern[:position] + colour_char + self._pattern[position + 1 :]
        )

        if self._pattern_changed_callback:
            self._pattern_changed_callback(self._pattern)

    def set_value(self, pattern, trigger_callback=True):
        """Set the current LED pattern
        :param trigger_callback: if False then the callback attached to this\
                control is not called
        """
        # type: (str, bool) -> None
        self._pattern = pattern

        for i, value in enumerate(pattern):
            if value == "O":
                self._green_radio_buttons[i].setSelected(True)
                self._red_radio_buttons[i].setSelected(True)
            elif value == "G":
                self._green_radio_buttons[i].setSelected(True)
                self._red_radio_buttons[i].setSelected(False)
            elif value == "R":
                self._green_radio_buttons[i].setSelected(False)
                self._red_radio_buttons[i].setSelected(True)
            else:
                self._green_radio_buttons[i].setSelected(False)
                self._red_radio_buttons[i].setSelected(False)

        if trigger_callback and self._pattern_changed_callback:
            self._pattern_changed_callback(pattern)

    def get_value(self):
        """Get the pattern that is currently set"""
        # type: () -> str
        return self._pattern

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._pattern_changed_callback = callback
        return False  # Don't use PyXBMCt's built in connection mechanism

    def _placedCallback(self, window, *args, **kwargs):
        super(LedPattern, self)._placedCallback(window, *args, **kwargs)

        label_alignment = pyxbmct.ALIGN_RIGHT | pyxbmct.ALIGN_CENTER_Y
        self.placeControl(
            pyxbmct.Label(self._label_text, alignment=label_alignment),
            0,
            3,
            columnspan=3,
        )

        self._green_radio_buttons = []
        self._red_radio_buttons = []
        for stage in range(1, 5):
            stage_label = pyxbmct.Label(
                "Stage " + str(stage), alignment=label_alignment
            )
            self.placeControl(stage_label, stage, 1, pad_x=-5)
            green_radio_button = pyxbmct.RadioButton("Green")
            self._green_radio_buttons.append(green_radio_button)
            red_radio_button = pyxbmct.RadioButton("Red")
            self._red_radio_buttons.append(red_radio_button)
            self.placeControl(green_radio_button, stage, 1)
            self.placeControl(red_radio_button, stage, 2)

            window.connect(
                green_radio_button,
                lambda pos=stage - 1: self._change_pattern_position(pos),
            )
            window.connect(
                red_radio_button,
                lambda pos=stage - 1: self._change_pattern_position(pos),
            )

        self.set_value(self._pattern, False)
