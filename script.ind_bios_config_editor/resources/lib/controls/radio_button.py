import pyxbmct
from .abstract_control import AbstractControl


class RadioButton(AbstractControl, pyxbmct.RadioButton):
    def __new__(cls, *args, **kwargs):
        return super(RadioButton, cls).__new__(cls, *args, **kwargs)

    def __init__(self, alignment=pyxbmct.ALIGN_RIGHT, *args, **kwargs):
        super(RadioButton, self).__init__(*args, **kwargs)
        self._value_set_callback = None

    def set_value(self, value, trigger_callback=True):
        super(RadioButton, self).setSelected(value)
        if trigger_callback and self._value_set_callback:
            self._value_set_callback(value)

    def get_value(self):
        return super(RadioButton, self).isSelected()

    def _connect_callback_wrapper(self, callback):
        self._value_set_callback = callback
        callback(self.get_value())

    def _connectCallback(self, callback, window):
        self._value_set_callback = callback
        return lambda: self._connect_callback_wrapper(callback)
