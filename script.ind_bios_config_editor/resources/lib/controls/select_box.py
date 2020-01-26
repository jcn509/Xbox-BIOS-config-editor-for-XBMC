from .button_with_icon import ButtonWithIcon
from .abstract_control import AbstractControl
import xbmcgui


class SelectBox(AbstractControl, ButtonWithIcon):

    def __new__(cls, options, default="", title="Select", *args, **kwargs):
        # Default is stored in the label
        return super(SelectBox, cls).__new__(cls, default, "menu_option.png", icon_pad_x=0, *args, **kwargs)

    def __init__(self, options, default="", title="Select", *args, **kwargs):
        super(SelectBox, self).__init__(default, "menu_option.png", icon_pad_x=0, *args, **kwargs)
        if not isinstance(options, list):
            raise TypeError("Options must be a list")
        if not all(isinstance(x, str) for x in options):
            raise TypeError("All options be strings")
        if not len(options) > 0:
            raise ValueError("Options must have at least one item")

        self._options = options
        self._title = title

    def get_value(self):
        return self.getLabel()

    def set_value(self, value, trigger_callback=True):
        if value not in self._options:
            raise ValueError("value must be in options")
        self._button.setLabel(value)
        if trigger_callback and self._option_chosen_callback:
            self._option_chosen_callback(value)

    def open_menu(self):
        current_value = self._button.getLabel()
        dialog = xbmcgui.Dialog()
        current_index = self._options.index(current_value)
        selected_index = dialog.select(self._title, self._options)
        # I don't think dialogs are garbage collected
        del dialog

        if selected_index != -1:
            selected_value = self._options[selected_index]
            self._button.setLabel(selected_value)
            if self._option_chosen_callback:
                self._option_chosen_callback(selected_value)

    def _connectCallback(self, callable, window):
        self._option_chosen_callback = callable
        return False

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(SelectBox, self)._placedCallback(window, *args, **kwargs)
        window.connect(self._button, self.open_menu)
