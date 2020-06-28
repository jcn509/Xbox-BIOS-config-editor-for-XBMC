"""Used to view tabs and choose which one should be displayed using a menu bar
"""
try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable, Dict, MutableMapping, Type, Union
    from ..configs import AbstractConfig
except:
   pass 

import pyxbmct

from .abstract_tab import AbstractTab
from .. import controls

class TabViewer(pyxbmct.Group):
    """Used to view tabs and choose which one should be displayed using a menu
    bar

    Uses lazy initialisation and so only creates tabs when they are actually
    needed for the first time.

    Note: calls window.autoNavigation whenever the user switches to a new tab
    (including when the viewer is first created and loads the first tab)!
    """
    
    def __new__(cls, config, total_size, menu_size, tabs, tab_icons = None, vertical_menu_bar = False, tab_switching_set_enabled_callback = None):
        num_columns = 1
        num_rows = total_size
        if vertical_menu_bar:
            num_rows, num_columns = num_columns, num_rows

        return super(TabViewer, cls).__new__(cls, num_rows, num_columns) 
        
    def __init__(self, config, total_size, menu_size, tabs, tab_icons = None, vertical_menu_bar = False, tab_switching_set_enabled_callback = None):
        """:param total_size: total number of columns in the grid layout if\
                vertical_menu_bar is True, otherwise the total number of rows
        :param menu_size: total number of columns that the menu bar takes up\
                if vertical_menu_bar is True otherwise the total number of\
                rows
        :param tabs: should be an ordered dict to ensure that the tab menu\
                buttons are in the correct order. Maps tab titles on to tab\
                classes
        :param tab_icons: optional, use it to define icons for the tab buttons
        :param icon_pad_x: the distance between the icons and the right edge\
                of the tab buttons
        :param vertical_menu_bar: if True create a vertical menu bar on the\
                left of the tab viewer otherwise create a horizontal one at\
                the top
        :param tab_switching_set_enabled_callback: callback to call when tab\
                switching is enabled or disabled
        """
        # type: (AbstractConfig, int, int, MutableMapping[str, AbstractTab], Dict[str, Union[str, pyxbmct.Image]], bool, Callable) -> None
        
        self._num_columns = 1
        self._num_rows = total_size
        if vertical_menu_bar:
            self._num_rows, self._num_columns = self._num_columns, self._num_rows

        super(TabViewer, self).__init__(self._num_rows, self._num_columns) 
        self._tab_switching_set_enabled_callback = tab_switching_set_enabled_callback

        self._config = config

        # Introduced this when I ran to issues if the user tried to switch tabs
        # too frequently. Stops the user from initiating a tab switch whilst
        # one is in progress
        self._tab_switching_enabled = True
        self._change_made_callback = None

        self._menu_size = menu_size
        self._vertical_menu_bar = vertical_menu_bar
        self._current_tab = tabs.keys()[0]
        
        self._tabs = tabs
        self._tab_icons = tab_icons

        # Not been placed yet
        self._window = None
    
    def setEnabled(self, enabled):
        """Have to overwrite this method to enable controls only on the
        current tab!

        Enable or disable all the controls in the tab viewer
        """
        # type: (bool) -> None 
        super(TabViewer, self).setEnabled(enabled)
        if enabled:
            for tab_name in self._tabs:
                if tab_name != self._current_tab:
                    tab = self._tabs[tab_name]
                    if isinstance(tab, AbstractTab):
                        tab.setEnabled(False)
            
            self._tab_menu_buttons[self._current_tab].setEnabled(False)

    def setVisible(self, is_visible):
        """Have to overwrite this method to only make controls on the
        current tab visible!

        Enable or disable all the controls in the tab viewer
        """
        # type: (bool) -> None
        super(TabViewer, self).setVisible(is_visible)
        if is_visible:
            for tab_name in self._tabs:
                if tab_name != self._current_tab:
                    tab = self._tabs[tab_name]
                    if isinstance(tab, AbstractTab):
                        tab.setVisible(False)

    def set_tab_switching_enabled(self, enabled):
        """Enable or disable tab switching"""
        # type: (bool) -> None
        self._tab_switching_enabled = enabled
        if self._tab_switching_set_enabled_callback is not None:
            self._tab_switching_set_enabled_callback(enabled)

    def _create_tab_menu_bar(self):
        """Create the menu bar used to choose which tab to view

        If vertical_menu_bar is True, it is created at the left of the tab
        viewer otherwise it is created at the top
        """
        # type () -> None
        tab_group_rows = 1
        tab_group_columns = len(self._tabs)
        if self._vertical_menu_bar:
            tab_group_rows, tab_group_columns = tab_group_columns, tab_group_rows
        tab_group = pyxbmct.Group(tab_group_rows, tab_group_columns)
        
        row_span = 1
        column_span = self._menu_size
        if self._vertical_menu_bar:
            row_span, column_span = column_span, row_span

        self.placeControl(
            tab_group, 0, 0, columnspan=column_span, rowspan=row_span, pad_x=0, pad_y=0
        )
        self._tab_menu_buttons = {}
        
        # if vertical_menu_bar then position is the row at which the
        # button should be placed. Otherwise it is the column
        for position, title in enumerate(self._tabs):
            button = None
            if self._tab_icons and title in self._tab_icons:
                button = controls.ButtonWithIcon(
                    title, self._tab_icons[title]
                )
            else:
                button = pyxbmct.Button(title)
            self._tab_menu_buttons[title] = button
            row = 0
            column = position
            if self._vertical_menu_bar:
                row, column = column, row
            tab_group.placeControl(button, row, column, pad_x=0, pad_y=0)
            self._window.connect(button, lambda tab=title: self.switch_tab(tab))
    
    def focus_tab_menu_button(self, tab_name):
        """Focus the menu button (in the menu bar) for the current tab"""
        # type (str) -> None
        self._window.setFocus(self._tab_menu_buttons[tab_name])

    def _hide_tab(self, tab_name):
        # type: (str) -> None
        self._tabs[tab_name].setVisible(False)
        self._tabs[tab_name].setEnabled(False)
    
    def _create_tab(self, tab_class):
        # type: (Type) -> AbstractTab
        tab = tab_class(self._config, self)

        row = self._menu_size
        column = 0
        if self._vertical_menu_bar:
            row, column = column, row
        
        row_span = 1 if self._vertical_menu_bar else (self._num_rows - self._menu_size)
        column_span = self._num_columns - self._menu_size if self._vertical_menu_bar else 1
        
        self.placeControl(tab, row, column, rowspan=row_span, columnspan = column_span)
        self._window.connect(tab, self._change_made_in_tab)

        return tab

    def _show_tab(self, tab_name):
        # type: (str) -> None
        tab = self._tabs[tab_name]

        # Tab has not been created yet.
        # We know this as it is a class
        # and not an instance of that class
        if isinstance(tab, type):
            self._tabs[tab_name] = self._create_tab(tab)
        else:
            tab.setVisible(True)
            tab.setEnabled(True)

    def switch_tab(self, tab_name):
        """Hide and disable the current tab and make the given tab visible and
        usable
        """
        # type: (str) -> None
        # Stops errors when the user switches tabs too fast
        if self._tab_switching_enabled and self._current_tab != tab_name:
            self.set_tab_switching_enabled(False)
            previous_tab = self._current_tab
            if previous_tab != None:
                self._tab_menu_buttons[previous_tab].setEnabled(True)
                self._hide_tab(previous_tab)
            
            self._show_tab(tab_name)

            # Perform navigation setup now before disabling the new tab
            # button so that it is set up such that the control xbmc thinks
            # is below/next to it can be one from the new tab
            self._window.autoNavigation()

            self._tab_menu_buttons[tab_name].setEnabled(False)
           
            # Need to redo navigation after the old tab button is hidden
            # as no controls can have it defined as what is above them. If
            # they do then as it is disabled XBMC will then choose whatever
            # is defined as the control above that one, which is wierd.
            self._window.autoNavigation()

            self._current_tab = tab_name

            self.set_tab_switching_enabled(True)
    
    def _change_made_in_tab(self, field, value):
        # type: (str, Any) -> None
        if self._change_made_callback is not None:
            self._change_made_callback(field, value)

    def _connectCallback(self, callback, window):
        # type: (Callable, Any) -> bool
        self._change_made_callback = callback
        return False # Don't use PyXBMCt's built in connection mechanism

    def _placedCallback(self, window, *args, **kwargs):
        super(TabViewer, self)._placedCallback(window, *args, **kwargs)
        self._window = window

        self._create_tab_menu_bar()

        # At this time all elements in this dict are classes
        # that are to be used to create the tabs
        first_tab = self._current_tab
        self._current_tab = None # Don't try to hide the current tab
        self.switch_tab(first_tab)

