import xbmc
import xbmcgui
from .button_with_icon import ButtonWithIcon
from .abstract_control import AbstractControl


class FakeEdit(AbstractControl, ButtonWithIcon):
    """
        FakeEdit(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
        
        Not a derivate of ControlEdit class.
        
        Implements a text entry box.
        
        :param default: string -- default value.
        :param update_label_on_enter: booelean -- change label value to what is entered.
        :param texturefocus: string -- image filename.
        
        .. note:: After you create the control, you need to add it to the window with placeControl().
        
        Example::
        
            self.edit = FakeEdit()
        """

    def __new__(cls, default="Enter something...", update_label_on_enter=True,
                type=0, heading="Enter something...", option=0,
                icon_pad_x=12, *args, **kwargs):

        return super(FakeEdit, cls).__new__(cls, default, "edit.png", icon_pad_x=icon_pad_x, *args, **kwargs)

    def __init__(self, default="Enter something...", update_label_on_enter=True,
                 type=0, heading="Enter something...", option=0,
                 icon_pad_x=12, *args, **kwargs):
        super(FakeEdit, self).__init__(default, "edit.png", icon_pad_x=icon_pad_x, *args, **kwargs)
        self._type = type
        self._heading = heading
        self._option = option
        self._update_label_on_enter = update_label_on_enter
        self._current_value = default

        self._value_chosen_callback = None

    def get_value(self):
        return self._current_value

    def set_value(self, value, trigger_callback=True):
        if self._update_label_on_enter:
            self._button.setLabel(value)

        self._current_value = value
        if trigger_callback and self._value_chosen_callback:
            self._value_chosen_callback(value)

    def enter_value(self):
        keyboard = xbmc.Keyboard(self._current_value, self._heading)
        keyboard.doModal()
        if keyboard.isConfirmed():
            value = keyboard.getText()

            if value != self._current_value:
                self.set_value(value)

        # Not sure if this is garbage collected?            
        del keyboard

    def _connectCallback(self, callable, window):
        self._value_chosen_callback = callable
        return False

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(FakeEdit, self)._placedCallback(window, *args, **kwargs)
        window.connect(self._button, self.enter_value)
