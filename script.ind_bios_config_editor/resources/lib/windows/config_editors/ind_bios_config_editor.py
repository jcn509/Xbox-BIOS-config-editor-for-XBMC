"""Config editor window for the iND-BiOS config file"""
from collections import namedtuple, OrderedDict

from .abstract_config_editor import AbstractConfigEditor, TabConfig
from ...tabs import ind_bios
from collections import OrderedDict
from ... import configs


class IndBiosConfigEditor(AbstractConfigEditor):
    """Config editor window for the iND-BiOS config file"""

    def _create_tab_data(self):
        # type: () -> TabConfig
        tab_names = namedtuple("TabNames", ("basic", "boot", "flubber", "x_screen", "advanced"))("Basic", "Boot", "Flubber", "X Screen", "Advanced")
      
        return TabConfig(
            OrderedDict((
                (tab_names.basic, ind_bios.Basic),
                (tab_names.boot, ind_bios.Boot),
                (tab_names.flubber, ind_bios.Flubber),
                (tab_names.x_screen, ind_bios.XScreen),
                (tab_names.advanced, ind_bios.Advanced)
            )),
            OrderedDict((
                (tab_names.basic, "settings.png"),
                (tab_names.boot, "dashboard.png"),
                (tab_names.flubber, "video_camera_round.png"),
                (tab_names.x_screen, "close.png"),
                (tab_names.advanced, "option_bar_settings.png")
            )),
            ind_bios.AbstractIndBiosTab.NUM_ROWS, 
        )

    def _create_config(self):
        # type () -> configs.IndBiosConfig
        return configs.IndBiosConfig()

    def _get_window_title(self):
        # type: () -> str
        return "iND-BiOS Config Editor"
