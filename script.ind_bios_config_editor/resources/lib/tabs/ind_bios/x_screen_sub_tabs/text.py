import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class Text(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Text, self).__init__(config, tab_viewer, 6)

    def _create_controls(self):
        self._place_and_link("IND3D", controls.RadioButton("iND 'XBOX' text"), 0, 0)
        self._place_label("'XBOX' text colour", 0, 1)
        self._place_and_link(
            "XBOXCOLOR", controls.ColourPicker("'XBOX' text colour"), 0, 2
        )
        self._place_label("Text Scale", 0, 3)
        self._place_and_link(
            "TEXTSCALE",
            controls.FakeSlider(
                min_value=0, max_value=100, keyboard_title="Text Scale"
            ),
            0,
            4,
            columnspan=2,
        )
        self._place_label("Custom 'XBOX' text", 1, 0)
        self._place_and_link(
            "CUSTOMTEXT",
            controls.FileSelectorOrZero(
                file_select_window_title="Custom 'XBOX' text", mask=".x"
            ),
            1,
            1,
            columnspan=5,
        ) 
