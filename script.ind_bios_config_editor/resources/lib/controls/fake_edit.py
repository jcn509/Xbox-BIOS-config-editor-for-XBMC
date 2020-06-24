"""A text box control"""
try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass
import xbmc
import xbmcgui
from .button_with_icon import ButtonWithIcon
from .abstract_control import AbstractControl


class FakeEdit(AbstractControl, ButtonWithIcon):
    """A text box control that uses a popup keyboard

    Not a derivative of ControlEdit class as that is not available on XBMC4Xbox
    """

    def __new__(
        cls,
        default_value="Enter something...",
        update_label_on_enter=True,
        keyboard_title="Enter something...",
        icon_pad_x=12,
        *args,
        **kwargs
    ):
        return super(FakeEdit, cls).__new__(
            cls, default_value, "edit.png", icon_pad_x=icon_pad_x, *args, **kwargs
        )

    def __init__(
        self,
        default_value="Enter something...",
        update_label_on_enter=True,
        keyboard_title="Enter something...",
        icon_pad_x=12,
        *args,
        **kwargs
    ):
        """:param default: default value.
        :param update_label_on_enter: change button label value to what is entered.
        :param keyboard_title: the title displayed on the popup keyboard window
        """
        # type: (str, bool, str, int, Any, Any) -> None
        super(FakeEdit, self).__init__(
            default_value, "edit.png", icon_pad_x=icon_pad_x, *args, **kwargs
        )
        self._keyboard_title = keyboard_title
        self._update_label_on_enter = update_label_on_enter
        self._current_value = default_value

        self._value_chosen_callback = None

    def get_value(self):
        """:returns: the text that has been entered"""
        # type: () -> str
        return self._current_value

    def set_value(self, value, trigger_callback=True):
        """set the entered text
        :param trigger_callback: if False then the whatever callback is\
                connected to this control is not called
        """
        # type: (str, bool) -> None
        if self._update_label_on_enter:
            self._button.setLabel(value)

        self._current_value = value
        if trigger_callback and self._value_chosen_callback:
            self._value_chosen_callback(value)

    def enter_value(self):
        """Bring up a keyboard so that the user can type in a new value"""
        # type: () -> None
        keyboard = xbmc.Keyboard(self._current_value, self._keyboard_title)
        keyboard.doModal()
        if keyboard.isConfirmed():
            value = keyboard.getText()

            if value != self._current_value:
                self.set_value(value)

        # Not sure if this is garbage collected?
        del keyboard

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._value_chosen_callback = callback
        return False # Don't use PyXBMCt's inbuilt connection mechanism

    def _placedCallback(self, window, *args, **kwargs):
        super(FakeEdit, self)._placedCallback(window, *args, **kwargs)
        window.connect(self._button, self.enter_value)
