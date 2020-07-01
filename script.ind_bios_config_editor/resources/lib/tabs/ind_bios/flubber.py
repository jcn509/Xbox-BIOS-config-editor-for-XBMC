from collections import namedtuple, OrderedDict

import pyxbmct

from .abstract_ind_bios_tab import AbstractIndBiosTab
from ... import controls
from .flubber_sub_tabs import Background, Blob, Fog, General, Glow
from ..tab_viewer import TabViewer

class Flubber(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Flubber, self).__init__(config, tab_viewer, 2)

    def _create_controls(self):
        self._place_load_preset_button(0, 0)
        self._place_save_preset_button(0, 1)
       
        tab_names = namedtuple("TabNames", ("background", "blob", "fog", "general", "glow"))("Background", "Blob", "Fog", "General", "Glow")

        tabs = OrderedDict((
            (tab_names.general, General),
            (tab_names.background, Background),
            (tab_names.blob, Blob),
            (tab_names.fog, Fog),
            (tab_names.glow, Glow),
        ))
        tab_icons = OrderedDict((
            (tab_names.general, "control.png"),
            (tab_names.background, "cover_flow.png"),
            (tab_names.blob, "atom.png"),
            (tab_names.fog, "cloud.png"),
            (tab_names.glow, "brightness.png"),
        ))

        self._sub_tab_viewer = TabViewer(self._config, 5, 1, tabs, tab_icons=tab_icons, vertical_menu_bar=True, tab_switching_set_enabled_callback=self._tab_viewer.set_tab_switching_enabled)
        self.placeControl(self._sub_tab_viewer, 1, 0, columnspan=2, rowspan=self.NUM_ROWS-1)
        self._window.connect(self._sub_tab_viewer, self._call_value_changed_callback_if_exists)
