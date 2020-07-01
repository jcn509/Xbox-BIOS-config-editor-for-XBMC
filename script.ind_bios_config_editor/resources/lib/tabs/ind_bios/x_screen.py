from collections import namedtuple, OrderedDict

import pyxbmct

from .abstract_ind_bios_tab import AbstractIndBiosTab
from ... import controls
from .x_screen_sub_tabs import General, Text, MSLogo, XLogo
from ..tab_viewer import TabViewer

class XScreen(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(XScreen, self).__init__(config, tab_viewer, 2)

    def _create_controls(self):
        self._place_load_preset_button(0, 0)
        self._place_save_preset_button(0, 1)
       
        tab_names = namedtuple("TabNames", ("general", "text", "ms_logo", "x_logo"))("General", "Text", "MS Logo", "X Logo")

        tabs = OrderedDict((
            (tab_names.general, General),
            (tab_names.x_logo, XLogo),
            (tab_names.text, Text),
            (tab_names.ms_logo, MSLogo),
        ))
        tab_icons = OrderedDict((
            (tab_names.general, "control.png"),
            (tab_names.x_logo, "close_2.png"),
            (tab_names.text, "edit_text_bar.png"),
            (tab_names.ms_logo, "microsoft.png"),
        ))

        self._sub_tab_viewer = TabViewer(self._config, 5, 1, tabs, tab_icons=tab_icons, vertical_menu_bar=True, tab_switching_set_enabled_callback=self._tab_viewer.set_tab_switching_enabled)
        self.placeControl(self._sub_tab_viewer, 1, 0, columnspan=2, rowspan=self.NUM_ROWS-1)
        self._window.connect(self._sub_tab_viewer, self._call_value_changed_callback_if_exists)
