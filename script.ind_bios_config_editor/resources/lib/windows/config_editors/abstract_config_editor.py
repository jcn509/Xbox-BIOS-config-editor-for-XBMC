"""Abstract config editor window. Contains common functionality"""

from collections import OrderedDict
from abc import ABCMeta, abstractmethod

try:
    # typing is not available on XBMC4Xbox
    from typing import Any

    # For typing purposes only
    from ...configs import AbstractConfig
except:
    pass

import xbmcgui
import pyxbmct

from ... import controls
from .reset_to_default import ResetToDefault
from ...tabs import TabViewer

class AbstractConfigEditor(pyxbmct.AddonDialogWindow):
    """Abstract config editor window. Contains common functionality"""

    __metaclass__ = ABCMeta

    # Using __new__ here is necessary otherwise config_filename gets passed to
    # some ancestor class which causes an error
    def __new__(cls, config_filename, *args, **kwargs):
        return super(AbstractConfigEditor, cls).__new__(cls, *args, **kwargs)

    def __init__(self, config_filename, *args, **kwargs):
        # type: (str, Any, Any) -> None
        super(AbstractConfigEditor, self).__init__(self._get_window_title())
        
        # Use 720P coordinate resolution this way everything should look
        # the same at any resolution rather than being super huge on standard
        # def displays.
        self.setCoordinateResolution(1)

        self._config_filename = config_filename
        tab_data = self._create_tab_data()
        tabs = tab_data["tabs"]
        tab_rows = tab_data["tab_rows"]

        self._num_rows = tab_rows + 2
        self._num_columns = 1
        self._config = self._create_config()
        self._config.read(config_filename)
        self._unsaved_changes = False

        self._last_preset_filename = None

        self.setGeometry(1200, 640, self._num_rows, self._num_columns)
        
        # Note: navigation is configured whenever the current tab is changed
        # so there is no need to set it up now as we are about to display
        # the first tab anyway...
        self._create_menu_bar(self._num_rows - 1, self._num_columns)
        
        tab_viewer = TabViewer(tab_rows, 1, tabs)
        self.placeControl(tab_viewer, 1, 0, row_span = tab_rows)
        tab_viewer.focus_current_tab_menu_button()
        self.connect(tab_viewer, self._change_made_in_tab)

        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    @abstractmethod
    def _create_tab_data(self):
        pass

    @abstractmethod
    def _create_config(self):
        # type: () -> AbstractConfig
        pass

    @abstractmethod
    def _get_window_title(self):
        # type: () -> str
        pass

    def close(self):
        # type: () -> None
        close = True
        if self._unsaved_changes:
            dialog = xbmcgui.Dialog()
            close = dialog.yesno(
                "Unsaved Changes!",
                "You have unsaved changes!",
                "Are you sure you want to close this app?",
            )
            del dialog

        if close:
            super(AbstractConfigEditor, self).close()

    def save_config(self):
        """Save the config to the HDD. Creates a popup dialogue window that
        asks for confirmation first
        """
        # type: () -> None
        dialog = xbmcgui.Dialog()
        save = dialog.yesno(
            "Save Changes?",
            "Are you sure you want to save your changes?",
            "This WILL overwrite your existing config!",
        )
        del dialog
        if save:
            self._unsaved_changes = False
            with open(self._config_filename, "w") as config_file:
                self._config.write(config_file)

    def reset_to_default(self, tab_names):
        """Reset these tabs to default"""
        for tab in tab_names:
            self._tab_groups[tab].reset_to_default()

    def _reset_to_default_button_clicked(self):
        # type: () -> None
        reset_to_default_window = ResetToDefault(
            self._tab_groups.keys(), self.reset_to_default
        )
        reset_to_default_window.doModal()
        del reset_to_default_window

    def _change_made_in_tab(self, field, value):
        """Callback for when some change is made in some tab"""
        # type: (str, Any) -> None
        self._unsaved_changes = True
 
    def _create_menu_bar(self, row, num_cols):
        # type: (int, int) -> None
        self._menu_bar_buttons = {}

        menu_group = pyxbmct.Group(1, 2)
        self.placeControl(menu_group, row, 0, columnspan=num_cols, pad_x=0, pad_y=0)

        icon_pad_x = 7
        self._save_button = controls.ButtonWithIcon(
            "Save Config", "save_item.png", icon_pad_x=icon_pad_x
        )
        menu_group.placeControl(self._save_button, 0, 0)
        self.connect(self._save_button, self.save_config)
        self._menu_bar_buttons["Save Config"] = self._save_button

        self._reset_button = controls.ButtonWithIcon(
            "Reset To Default", "arrow_repeat.png", icon_pad_x=icon_pad_x
        )
        menu_group.placeControl(self._reset_button, 0, 1)
        self.connect(self._reset_button, self._reset_to_default_button_clicked)
        self._menu_bar_buttons["Reset To Default"] = self._reset_button

    def setAnimation(self, control):
        """Override of the PyXBMCt method (hence the camelCase)"""
        # Set fade animation for all add-on window controls
        control.setAnimations(
            [
                ("WindowOpen", "effect=fade start=0 end=100 time=500",),
                ("WindowClose", "effect=fade start=100 end=0 time=500",),
            ]
        )
