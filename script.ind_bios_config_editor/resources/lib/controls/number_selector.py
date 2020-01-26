import pyxbmct
import xbmcgui
from .abstract_control import AbstractControl

class NumberSelector(AbstractControl, pyxbmct.Button):
    def __new__(cls, min_value = 0, max_value = 255, default_value = None, step = 1, enable_scrolling = True, left_padding = "< ", right_padding = " >", picker_title = "Enter Number", *args, **kwargs):         
        return super(NumberSelector, cls).__new__(cls, "", *args, **kwargs)
        
    def __init__(self, min_value = 0, max_value = 255, default_value = None, step = 1, enable_scrolling = True, left_padding = "< ", right_padding =" >", picker_title = "Enter Number", *args, **kwargs):
        if max_value < min_value:
            raise ValueError("max_value must be >= min_value")
        if default_value == None:
            default_value = min_value
        if default_value > max_value:
            raise ValueError("default_value must be <= max_value")
        if default_value < min_value:
            raise ValueError("default_value must be >= min_value")
        
        self._value_changed_callback = None
        self._step = step
        self._min_value = min_value
        self._max_value = max_value
        self._left_padding = left_padding
        self._right_padding = right_padding
        self.set_value(default_value, False)

        self._picker_title = picker_title
        self._enable_scrolling = enable_scrolling

    def add_to_button_value(self, num_to_add):
        num = self.get_value()
        num += num_to_add
        self.set_value(num)

    def _add_to_button_value_focussed(self, num_to_add):
        if self._window.getFocus() == self:
            self.add_to_button_value(num_to_add)

    def _increase_if_focussed(self):
        self._add_to_button_value_focussed(self._step)

    def _decrease_if_focussed(self):
        self._add_to_button_value_focussed(-self._step)

    def get_value(self):
        return int(self.getLabel().replace(self._left_padding,"").replace(self._right_padding,""))

    def pick_value(self):
        dialog = xbmcgui.Dialog()
        self.set_value(int(dialog.numeric(0, self._picker_title, str(self.get_value()))))

        # I believe these aren't garbage collected?
        del dialog

    def set_value(self, value, trigger_callback = True):
        if value < self._min_value:
            value = self._min_value
        elif value > self._max_value:
            value = self._max_value

        self.setLabel(self._left_padding  + str(value) + self._right_padding)
        if trigger_callback and self._value_changed_callback:
            self._value_changed_callback(value)

    def _connectCallback(self, callback, window):
        self._value_changed_callback = callback
        return False

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        self._window = window

        # Need to temporarily disable _connectCallback so that it is not
        # triggered when window.connect is called below
        temp = self._connectCallback
        self._connectCallback = lambda x,y: True
        window.connect(self, self.pick_value)
        self._connectCallback = temp
        
        if self._enable_scrolling:
            window.connectEventList(
                [pyxbmct.ACTION_MOVE_RIGHT, pyxbmct.ACTION_MOUSE_WHEEL_UP],
                self._increase_if_focussed)
            window.connectEventList(
                [pyxbmct.ACTION_MOVE_LEFT,pyxbmct.ACTION_MOUSE_WHEEL_DOWN],
                self._decrease_if_focussed)

    def _removedCallback(self, window):
        if self._enable_scrolling:
            window.disconnectEventList(
                [pyxbmct.ACTION_MOVE_RIGHT, pyxbmct.ACTION_MOUSE_WHEEL_UP],
                self._increase_if_focussed)
            window.disconnectEventList(
                [pyxbmct.ACTION_MOVE_LEFT,pyxbmct.ACTION_MOUSE_WHEEL_DOWN],
                self._decrease_if_focussed)
