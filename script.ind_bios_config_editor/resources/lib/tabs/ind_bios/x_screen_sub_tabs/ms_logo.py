import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class MSLogo(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(MSLogo, self).__init__(config, tab_viewer, 6)

    def _create_controls(self):
        self._place_and_link("SHOWMSEN", controls.RadioButton("Show 'MS' logo"), 0, 0, columnspan=6)
        self._place_and_link(
            "MSLOGOTRANSEN",
            controls.RadioButton("Use transparency colour for 'MS' logo"),
            1,
            0,
            columnspan=6,
        )
        self._place_label("Transparency colour", 2, 0)
        self._place_and_link(
            "MSLOGOTRANSCOLOR", controls.ColourPicker("Transparency colour"), 2, 1, columnspan=5
        )
        self._place_label("'MS' logo X change", 3, 0)
        self._place_and_link(
            "XSKEWLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'MS' logo X change"
            ),
            3,
            1,
            columnspan=2,
        )
        self._place_label("'MS' logo Y change", 3, 3)
        self._place_and_link(
            "YSKEWLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'MS' logo Y change"
            ),
            3,
            4,
            columnspan=2,
        )
        self._place_label("Custom 'MS' logo", 4, 0)
        self._place_and_link(
            "CUSTOMLOGO",
            controls.FileSelectorOrZero(
                file_select_window_title="Custom 'MS' logo",
                mask=".bmp",
                use_thumbs=True,
            ),
            4,
            1,
            columnspan=5,
        )
