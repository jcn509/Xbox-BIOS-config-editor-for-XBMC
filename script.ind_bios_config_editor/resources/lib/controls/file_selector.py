from .button_with_icon import ButtonWithIcon
import xbmcgui
from .abstract_control import AbstractControl


def _get_icon_filename(type, custom_icon):
    if custom_icon:
        return custom_icon
    return "folder.png" if type in [0, 3] else "file.png"


class FileSelector(AbstractControl, ButtonWithIcon):

    def __new__(cls, default="Select File", update_label_on_select=True,
                type=1, heading="Select File", shares="files", mask="",
                use_thumbs=False, treat_as_folder=False, custom_icon=None,
                icon_pad_x=8, icon_pad_y=5, *args, **kwargs):
        icon = _get_icon_filename(type, custom_icon)
        return super(FileSelector, cls).__new__(cls, default, icon, icon_pad_x=10, *args, **kwargs)

    def __init__(self, default="Select File", update_label_on_select=True,
                 type=1, heading="Select File", shares="files", mask="",
                 use_thumbs=False, treat_as_folder=False, custom_icon=None,
                 icon_pad_x=8, icon_pad_y=5, *args, **kwargs):
        icon = _get_icon_filename(type, custom_icon)
        super(FileSelector, self).__init__(default, icon,
                                           icon_pad_x=icon_pad_x,
                                           icon_pad_y=icon_pad_y,
                                           *args, **kwargs)
        self._type = type
        self._heading = heading
        self._shares = shares
        self._mask = mask
        self._use_thumbs = use_thumbs
        self._treat_as_folder = treat_as_folder
        self._update_label_on_select = update_label_on_select
        self._current_selection = default

        self._file_chosen_callback = None

    def get_value(self):
        return self._current_selection

    def set_value(self, file_path, trigger_callback=True):
        if self._update_label_on_select:
            self._button.setLabel(file_path)

        self._current_selection = file_path

        if trigger_callback and self._file_chosen_callback:
            self._file_chosen_callback(file_path)

    def _browse(self):
        dialog = xbmcgui.Dialog()
        file_path = dialog.browse(self._type, self._heading, self._shares,
                                  self._mask, self._use_thumbs, self._treat_as_folder,
                                  self._current_selection)

        # I don't believe these are garbage collected?
        del dialog

        if file_path != self._current_selection:
            self.set_value(file_path)

    def _connectCallback(self, callable, window):
        self._file_chosen_callback = callable
        return False

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(FileSelector, self)._placedCallback(window, *args, **kwargs)
        window.connect(self._button, self._browse)
