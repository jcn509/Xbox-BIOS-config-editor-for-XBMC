import pyxbmct
from ... import controls
from .abstract_ind_bios_tab import AbstractIndBiosTab


class Advanced(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Advanced, self).__init__(config, tab_viewer, 2)

    def _create_controls(self):
        self._place_and_link(
            "USEALLMEMORY",
            controls.RadioButton("Use 128mb of Ram (if Available)"),
            0,
            0,
            columnspan=2,
        ),
        self._place_and_link(
            "DISABLEDM",
            controls.RadioButton("Disable debug monitor"),
            1,
            0,
            columnspan=2,
        )
        self._place_label(
            "Change MAC Address Note: 00:00:00:00:00:00 = From eeprom", 2, 0
        )
        self._place_and_link(
            "MACADDR",
            controls.FakeEdit(
                default_value="00:00:00:00:00:00",
                keyboard_title="Change MAC Address Note: 00:00:00:00:00:00 = From eeprom",
            ),
            2,
            1,
        ),
