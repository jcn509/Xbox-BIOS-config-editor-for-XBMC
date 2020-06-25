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

        self._config_filename = config_filename
        self._current_tab = None
        self._tab_switching_enabled = True
        tab_data = self._create_tab_data()
        self.NUM_ROWS = tab_data["num_rows"]
        form_config = tab_data["tabs"]
        self.NUM_ROWS += 2
        self.NUM_COLUMNS = 1
        self._config = self._create_config()
        self._config.read(config_filename)
        self._unsaved_changes = False

        self._last_preset_filename = None

        self.setGeometry(1200, 640, self.NUM_ROWS, self.NUM_COLUMNS)
        self._create_tabs(form_config)

        self._create_menu_bar(self.NUM_ROWS - 1, self.NUM_COLUMNS)

        self._initialise_navigation()
        first_tab = self._tab_groups.keys()[0]
        self.setFocus(self._tab_menu_buttons[first_tab])
        self.switch_tab(first_tab)

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

    def _create_tabs(self, form_config):
        """Create all the tabs that are displayed"""
        self._tab_groups = OrderedDict()

        for tab in form_config:
            tab_group = form_config[tab]["tab"](self._config)
            self.connect(tab_group, self._change_made_in_tab)
            self._tab_groups[tab] = tab_group
            self.placeControl(
                tab_group, 1, 0, columnspan=self.NUM_COLUMNS, rowspan=self.NUM_ROWS - 2
            )
            self._hide_tab(tab)

        self._create_tab_menu_bar(form_config)

    def _create_tab_menu_bar(self, form_config):
        tab_group = pyxbmct.Group(1, len(self._tab_groups))
        self.placeControl(
            tab_group, 0, 0, columnspan=self.NUM_COLUMNS, pad_x=0, pad_y=0
        )
        self._tab_menu_buttons = {}

        for col, title in enumerate(self._tab_groups):
            button = controls.ButtonWithIcon(
                title, form_config[title]["icon"], icon_pad_x=9
            )
            self._tab_menu_buttons[title] = button
            tab_group.placeControl(button, 0, col, pad_x=0, pad_y=0)
            self.connect(button, lambda tab=title: self.switch_tab(tab))

    def _initialise_navigation(self):
        """Set up the navigation between all the controls"""
        # type: () -> None
        # Some initialisation is done further down
        self._tab_menu_buttons_control_down = {}
        self._menu_bar_buttons_control_up = {}
        control_down_methods = {}
        control_up_methods = {}
        current_tab = ""
        for button_title in self._tab_menu_buttons:
            button = self._tab_menu_buttons[button_title].get_button()
            control_down_methods[button_title] = button.controlDown

            def new_control_down(control, button=button_title):
                control_down_methods[button](control)
                self._tab_menu_buttons_control_down[current_tab][button] = control

            button.controlDown = new_control_down

        for button_title in self._menu_bar_buttons:
            button = self._menu_bar_buttons[button_title].get_button()
            control_up_methods[button_title] = button.controlUp

            def new_control_up(control, button=button_title):
                control_up_methods[button](control)
                self._menu_bar_buttons_control_up[current_tab][button] = control

            button.controlUp = new_control_up

        for tab_title in self._tab_groups:
            current_tab = tab_title
            self._tab_menu_buttons_control_down[tab_title] = {}
            self._menu_bar_buttons_control_up[tab_title] = {}
            self._show_tab(tab_title)
            self.autoNavigation()
            self._hide_tab(tab_title)

        for button_title in self._tab_menu_buttons:
            button = self._tab_menu_buttons[button_title].get_button()
            button.controlDown = control_down_methods[button_title]

        for button_title in self._menu_bar_buttons:
            button = self._menu_bar_buttons[button_title].get_button()
            button.controlUp = control_up_methods[button_title]

    def _hide_tab(self, tab_name):
        self._tab_groups[tab_name].setVisible(False)
        self._tab_groups[tab_name].setEnabled(False)

    def _show_tab(self, tab_name):
        self._tab_groups[tab_name].setVisible(True)
        self._tab_groups[tab_name].setEnabled(True)

    def switch_tab(self, tab_name):
        """Hide and disable the current tab and make the given tab visible and
        usable
        """
        # type: (str) -> None
        # Stops errors when the user switches tabs too fast
        if self._tab_switching_enabled and self._current_tab != tab_name:
            self._tab_switching_enabled = False
            previous_tab = self._current_tab
            if previous_tab != None:
                self._tab_menu_buttons[previous_tab].setEnabled(True)
                self._hide_tab(previous_tab)

            self._show_tab(tab_name)

            for button_title in self._tab_menu_buttons:
                button = self._tab_menu_buttons[button_title].get_button()
                button.controlDown(
                    self._tab_menu_buttons_control_down[tab_name][button_title]
                )

            for button_title in self._menu_bar_buttons:
                button = self._menu_bar_buttons[button_title].get_button()
                button.controlUp(
                    self._menu_bar_buttons_control_up[tab_name][button_title]
                )

            self._tab_menu_buttons[tab_name].setEnabled(False)

            self._current_tab = tab_name

            self._tab_switching_enabled = True

    def _create_menu_bar(self, row, num_cols):
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
