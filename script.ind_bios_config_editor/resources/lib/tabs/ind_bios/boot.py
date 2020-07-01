import pyxbmct
from ... import controls
from .abstract_ind_bios_tab import AbstractIndBiosTab


class Boot(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Boot, self).__init__(config, tab_viewer, 10)

    def _create_controls(self):
        self._place_label("Dash 1", 0, 0)
        self._place_and_link(
            "DASH1",
            controls.FileSelector(file_select_window_title="Dash 1", mask=".xbe"),
            0,
            1,
            columnspan=9,
        )
        self._place_label("Dash 2", 1, 0)
        self._place_and_link(
            "DASH2",
            controls.FileSelector(file_select_window_title="Dash 2", mask=".xbe"),
            1,
            1,
            columnspan=9,
        )
        self._place_label("Dash 3", 2, 0)
        self._place_and_link(
            "DASH3",
            controls.FileSelector(file_select_window_title="Dash 3", mask=".xbe"),
            2,
            1,
            columnspan=9,
        )
        self._place_label("Default XBE", 3, 0)
        self._place_and_link(
            "DEFAULTXBE",
            controls.FakeEdit(
                default_value="Default XBE", keyboard_title="Default XBE"
            ),
            3,
            1,
            columnspan=9,
        )

        self._place_and_link(
            "INTRO",
            controls.RadioButton("Show intro (flubber and 'x' screen)"),
            4,
            0,
            columnspan=5,
        )
        self._place_and_link(
            "USEXBX",
            controls.RadioButton("Use Debug XBX file for Dash Load"),
            4,
            5,
            columnspan=5,
        )
