"""A popup menu/select box control"""
try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable, Tuple
except:
    pass

import xbmcgui

from .button_with_icon import ButtonWithIcon
from .abstract_control import AbstractControl


class SelectBox(AbstractControl, ButtonWithIcon):
    """A popup menu/select box control"""

    def __new__(cls, options, default="", popup_window_title="Select", *args, **kwargs):
        # Default is stored in the label
        return super(SelectBox, cls).__new__(
            cls, default, "menu_option.png", icon_pad_x=0, *args, **kwargs
        )

    def __init__(
        self, options, default="", popup_window_title="Select", *args, **kwargs
    ):
        # type: (Tuple[str], str, str, Any, Any) -> None
        super(SelectBox, self).__init__(
            default, "menu_option.png", icon_pad_x=0, *args, **kwargs
        )
        if not isinstance(options, list):
            raise TypeError("Options must be a list")
        if not all(isinstance(x, str) for x in options):
            raise TypeError("All options be strings")
        if not len(options) > 0:
            raise ValueError("Options must have at least one item")

        self._options = options
        self._popup_window_title = popup_window_title

    def get_value(self):
        """:returns: the option that is currently selected"""
        # type: () -> str
        return self.getLabel()

    def set_value(self, chosen_option, trigger_callback=True):
        """Set which option is currently chosen
        :param trigger_callback: if False then the callback that is attached\
                to this control is not called
        """
        # type: (str, bool) -> None
        if chosen_option not in self._options:
            raise ValueError(str(chosen_option) + " not a valid choice")
        self._button.setLabel(chosen_option)
        if trigger_callback and self._option_chosen_callback:
            self._option_chosen_callback(chosen_option)

    def open_menu(self):
        """Open the menu and allow the user to choose an option"""
        # type: () -> None
        current_value = self._button.getLabel()
        dialog = xbmcgui.Dialog()
        current_index = self._options.index(current_value)
        selected_index = dialog.select(self._popup_window_title, self._options)
        # I don't think dialogs are garbage collected
        del dialog

        if selected_index != -1:
            selected_value = self._options[selected_index]
            self._button.setLabel(selected_value)
            if self._option_chosen_callback:
                self._option_chosen_callback(selected_value)

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._option_chosen_callback = callback
        return False  # Don't use PyXBMCt's built in connection mechanism

    def _placedCallback(self, window, *args, **kwargs):
        super(SelectBox, self)._placedCallback(window, *args, **kwargs)
        window.connect(self._button, self.open_menu)
