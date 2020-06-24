"""Config editor window for the iND-BiOS config file"""

from .abstract_config_editor import AbstractConfigEditor
from ...tabs import ind_bios
from collections import OrderedDict
from ... import configs


class IndBiosConfigEditor(AbstractConfigEditor):
    """Config editor window for the iND-BiOS config file"""
    def _create_tab_data(self):
        tabs_dict = OrderedDict(
            [
                ("Basic", {"tab": ind_bios.Basic, "icon": "settings.png"}),
                (
                    "Boot Settings",
                    {"tab": ind_bios.BootSettings, "icon": "dashboard.png"},
                ),
                (
                    "Flubber",
                    {"tab": ind_bios.Flubber, "icon": "video_camera_round.png"},
                ),
                ("X Screen", {"tab": ind_bios.XScreen, "icon": "close.png"}),
                (
                    "Advanced",
                    {"tab": ind_bios.Advanced, "icon": "option_bar_settings.png"},
                ),
            ]
        )
        tab_data = {
            "tabs": tabs_dict,
            "num_rows": ind_bios.AbstractIndBiosTab.NUM_ROWS,
        }
        return tab_data

    def _create_config(self):
        # type () -> configs.IndBiosConfig
        return configs.IndBiosConfig()

    def _get_window_title(self):
        # type: () -> str
        return "iND-BiOS Config Editor"
