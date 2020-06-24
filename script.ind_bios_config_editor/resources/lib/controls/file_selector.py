"""A basic file selector control"""
try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable
except:
    pass

import xbmcgui

from .button_with_icon import ButtonWithIcon
from .abstract_control import AbstractControl


def _get_icon_filename(browse_type, custom_icon):
    if custom_icon:
        return custom_icon
    return "folder.png" if browse_type in [0, 3] else "file.png"


class FileSelector(AbstractControl, ButtonWithIcon):
    """Used to select files stored on the HDD or on DVD.

    Presents a button that shows the currently selected file. Clicking on the
    button brings up a dialogue window that is used to select a different file
    """
    def __new__(
        cls,
        default="Select File",
        update_label_on_select=True,
        browse_type=1,
        file_select_window_title="Select File",
        shares="files",
        mask="",
        use_thumbs=False,
        treat_as_folder=False,
        custom_icon=None,
        icon_pad_x=8,
        icon_pad_y=5,
        *args,
        **kwargs
    ):
        icon = _get_icon_filename(browse_type, custom_icon)
        return super(FileSelector, cls).__new__(
            cls, default, icon, icon_pad_x=10, *args, **kwargs
        )

    def __init__(
        self,
        default="Select File",
        update_label_on_select=True,
        browse_type=1,
        file_select_window_title="Select File",
        shares="files",
        mask="",
        use_thumbs=False,
        treat_as_folder=False,
        custom_icon=None,
        icon_pad_x=8,
        icon_pad_y=5,
        *args,
        **kwargs
    ):
        """Please also see the docs for xbmcgui.Dialog.browse
        :param default: the text to display/file to be selected by default
        :param update_label_on_select: update the label on the button when a\
                file is selected
        :param browse_type: see docs for xbmcgui.Dialog.browse
        :param file_select_window_title: the title to display in the dialog popup window
        :param shares: see docs for xbmcgui.Dialog.browse
        :param mask: see docs for xbmcgui.Dialog.browse
        :param use_thumbs: see docs for xbmcgui.Dialog.browse
        :param treat_as_folder: see docs for xbmcgui.Dialog.browse
        :param icon_pad_x: for the icon displayed on the button
        :param icon_pad_y: for the icon displayed on the button
        """
        # type: (str, bool, int, str, str, str, bool, bool, str, int, int, Any, Any) -> None
        icon = _get_icon_filename(browse_type, custom_icon)
        super(FileSelector, self).__init__(
            default, icon, icon_pad_x=icon_pad_x, icon_pad_y=icon_pad_y, *args, **kwargs
        )
        self._browse_type = browse_type
        self._file_select_window_title = file_select_window_title
        self._shares = shares
        self._mask = mask
        self._use_thumbs = use_thumbs
        self._treat_as_folder = treat_as_folder
        self._update_label_on_select = update_label_on_select
        self._current_selection = default

        self._file_chosen_callback = None

    def get_value(self):
        """:returns: the filename of the currently selected file"""
        # type: () -> str
        return self._current_selection

    def set_value(self, file_path, trigger_callback=True):
        """Set the currently selected file
        :param trigger_callback: if False then whatever callback is connected\
                to this control won't be called
        """
        # type: (str, bool) -> None
        if self._update_label_on_select:
            self._button.setLabel(file_path)

        self._current_selection = file_path

        if trigger_callback and self._file_chosen_callback:
            self._file_chosen_callback(file_path)

    def _browse(self):
        """Bring up the file browser dialogue window that is used to select a
        new file
        """
        # type: () -> None
        dialog = xbmcgui.Dialog()
        file_path = dialog.browse(
            self._browse_type,
            self._file_select_window_title,
            self._shares,
            self._mask,
            self._use_thumbs,
            self._treat_as_folder,
            self._current_selection,
        )

        # I don't believe these are garbage collected?
        del dialog

        if file_path != self._current_selection:
            self.set_value(file_path)

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._file_chosen_callback = callback
        return False # Don't use PyXBMCt's built in connection mechanism

    def _placedCallback(self, window, *args, **kwargs):
        """
        Called once the button has been placed
        """
        super(FileSelector, self)._placedCallback(window, *args, **kwargs)
        window.connect(self._button, self._browse)
