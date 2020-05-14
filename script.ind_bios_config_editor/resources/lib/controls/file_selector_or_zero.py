from .file_selector import FileSelector
import pyxbmct
from .abstract_control import AbstractControl


class FileSelectorOrZero(AbstractControl, pyxbmct.Group):
    def __new__(
        cls, total_width=8, enable_width=1, enabled_by_default=True, *args, **kwargs
    ):
        return super(FileSelectorOrZero, cls).__new__(cls, 1, total_width)

    def __init__(
        self, total_width=8, enable_width=1, enabled_by_default=True, *args, **kwargs
    ):
        super(FileSelectorOrZero, self).__init__(1, total_width)
        self._total_width = total_width
        self._enable_width = enable_width
        self._file_selector = FileSelector(*args, **kwargs)
        self._enabled_by_default = enabled_by_default

        self._file_selected_callback = None
        self._file_path = None

    def _enabler_changed(self, trigger_callback=True):
        enabled = self._enabler.isSelected()
        self._file_selector.setEnabled(enabled)
        if trigger_callback and self._file_selected_callback:
            if enabled:
                if self._file_path:
                    self._file_selected_callback(self._file_path)
            else:
                self._file_selected_callback("0")

    def setEnabled(self, enabled):
        super(FileSelectorOrZero, self).setEnabled(enabled)
        if enabled:
            # Make sure that File Selector is disabled if it should be
            self._enabler_changed(False)

    def get_value(self):
        return self._file_selector.get_value()

    def set_value(self, selection, trigger_callback=True):
        if selection == "0":
            if self._enabler.isSelected():
                self._enabler.setSelected(False)
                self.enabler_changed()
        else:
            self._file_selector.set_value(selection, trigger_callback=trigger_callback)

    def _connectCallback(self, callable, window):
        self._file_selected_callback = callable

        def wrapped_callable(file_path):
            self._file_path = file_path
            callable(file_path)

        window.connect(self._file_selector, wrapped_callable)
        return False

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(FileSelectorOrZero, self)._placedCallback(window, *args, **kwargs)
        selector_width = self._total_width - self._enable_width
        self.placeControl(
            self._file_selector,
            0,
            self._enable_width,
            columnspan=selector_width,
            pad_x=0,
            pad_y=0,
        )

        self._enabler = pyxbmct.RadioButton("Enable")
        self.placeControl(self._enabler, 0, 0, pad_x=0, pad_y=0)
        self._enabler.setSelected(self._enabled_by_default)
        window.connect(self._enabler, self._enabler_changed)
