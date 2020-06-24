"""Simple wrapper for :pyxbmc.RadioButton: to ensure that it has the same
interface as the other controls
"""

try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass

import pyxbmct
from .abstract_control import AbstractControl


class RadioButton(AbstractControl, pyxbmct.RadioButton):
    """Simple wrapper for :pyxbmc.RadioButton: to ensure that it has the same
    interface as the other controls
    """
    def __new__(cls, *args, **kwargs):
        return super(RadioButton, cls).__new__(cls, *args, **kwargs)

    def __init__(self, alignment=pyxbmct.ALIGN_RIGHT, *args, **kwargs):
        super(RadioButton, self).__init__(*args, **kwargs)
        self._value_set_callback = None

    def set_value(self, value, trigger_callback=True):
        """Set the current value
        :param trigger_callback: if False then the callback attached to this\
                is not called
        """
        # type: (bool, bool) -> None
        super(RadioButton, self).setSelected(value)
        if trigger_callback and self._value_set_callback:
            self._value_set_callback(value)

    def get_value(self):
        """True if the radio button is on else False"""
        # type: () -> bool
        # isSelected seems to return a 1 or 0 rather than True or False
        return bool(super(RadioButton, self).isSelected())

    def _connect_callback_wrapper(self, callback):
        # type: (Callable) -> None
        self._value_set_callback = callback
        callback(self.get_value())

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> Callable
        # wrap the callback so that it will pass a boolean indicating if the
        # radio button is or not not to the outside world
        self._value_set_callback = callback
        return lambda: self._connect_callback_wrapper(callback)
