"""File selector control that allows the user to also select no file"""
try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass

import pyxbmct

from .file_selector import FileSelector
from .abstract_control import AbstractControl


class FileSelectorOrZero(AbstractControl, pyxbmct.Group):
    """File selector control that allows the user to also select no file"""
    
    def __new__(
        cls, total_width=8, enable_radio_button_width=1, enabled_by_default=True, *args, **kwargs
    ):
        return super(FileSelectorOrZero, cls).__new__(cls, 1, total_width)

    def __init__(
        self, total_width=8, enable_radio_button_width=1, enabled_by_default=True, *args, **kwargs
    ):
        """:param total_width: the number of columns used for the control
        :param enable_radio_button_width: width in columns of the\
                enable/disable radio button
        """
        # type: (int, int, bool, Any, Any) -> None
        super(FileSelectorOrZero, self).__init__(1, total_width)
        self._total_width = total_width
        self._enable_radio_button_width = enable_radio_button_width
        self._file_selector = FileSelector(*args, **kwargs)
        self._enabled_by_default = enabled_by_default

        self._file_selected_callback = None
        self._file_path = None

    def _enable_radio_button_changed(self, trigger_callback=True):
        """The enabled radio button has been toggled
        :param trigger_callback: if False the callback attached to this\
                control is not called
        """
        # type: (bool) -> None
        enabled = self._enable_radio_button.isSelected()
        self._file_selector.setEnabled(enabled)
        if trigger_callback and self._file_selected_callback:
            if enabled:
                if self._file_path:
                    self._file_selected_callback(self._file_path)
            else:
                self._file_selected_callback("0")

    def setEnabled(self, enabled):
        """Overrides the PyXBMCt method (hence the camelcase)"""
        # type: (bool) -> None
        super(FileSelectorOrZero, self).setEnabled(enabled)
        if enabled:
            # Make sure that File Selector is disabled if it should be
            self._enable_radio_button_changed(False)

    def get_value(self):
        """:returns: the currently chosen file or None if one is not chosen"""
        # type: () -> str
        return self._file_selector.get_value()

    def set_value(self, file_path, trigger_callback=True):
        """Set the currently chosen file
        :param file_path: set to None if no file is to be chosen
        :param trigger_callback: if False then the callback attached to this\
                control will not be called
        """
        if file_path == "0":
            if self._enable_radio_button.isSelected():
                self._enable_radio_button.setSelected(False)
                self.enable_radio_button_changed()
        else:
            self._file_selector.set_value(file_path, trigger_callback=trigger_callback)

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._file_selected_callback = callback
        
        # Delegate to the file selector if a file is chosen
        def wrapped_callable(file_path):
            self._file_path = file_path
            callback(file_path)

        window.connect(self._file_selector, wrapped_callable)
        return False # Don't use PyXBMCt's built in connection mechanism

    def _placedCallback(self, window, *args, **kwargs):
        super(FileSelectorOrZero, self)._placedCallback(window, *args, **kwargs)
        selector_width = self._total_width - self._enable_radio_button_width
        self.placeControl(
            self._file_selector,
            0,
            self._enable_radio_button_width,
            columnspan=selector_width,
            pad_x=0,
            pad_y=0,
        )

        self._enable_radio_button = pyxbmct.RadioButton("Enable")
        self.placeControl(self._enable_radio_button, 0, 0, pad_x=0, pad_y=0)
        self._enable_radio_button.setSelected(self._enabled_by_default)
        window.connect(self._enable_radio_button, self._enable_radio_button_changed)
