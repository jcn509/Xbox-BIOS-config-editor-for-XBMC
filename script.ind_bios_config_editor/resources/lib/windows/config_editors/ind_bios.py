from .abstract_config_editor import AbstractConfigEditor
from ... import tabs
from collections import OrderedDict
from ... import configs


class IndBiosConfigEditor(AbstractConfigEditor):
    def _create_tab_data(self):
        tabs_dict = OrderedDict(
            [
                ("Basic", {"tab": tabs.ind_bios.Basic, "icon": "settings.png"}),
                (
                    "Boot Settings",
                    {"tab": tabs.ind_bios.BootSettings, "icon": "dashboard.png"},
                ),
                (
                    "Flubber",
                    {"tab": tabs.ind_bios.Flubber, "icon": "video_camera_round.png"},
                ),
                ("X Screen", {"tab": tabs.ind_bios.XScreen, "icon": "close.png"}),
                (
                    "Advanced",
                    {"tab": tabs.ind_bios.Advanced, "icon": "option_bar_settings.png"},
                ),
            ]
        )
        tab_data = {
            "tabs": tabs_dict,
            "num_rows": tabs.ind_bios.AbstractIndBiosTab.NUM_ROWS,
        }
        return tab_data

    def _create_config(self):
        return configs.IndBiosConfig()

    def _get_window_title(self):
        return "iND-BiOS Config Editor"
