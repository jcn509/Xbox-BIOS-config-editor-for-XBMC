import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class XLogo(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(XLogo, self).__init__(config, tab_viewer, 6)

    def _create_controls(self):
        self._place_and_link("SHOWXEN", controls.RadioButton("Show 'X'"), 0, 0)

        self._place_label("'X' glow colour", 0, 1)
        self._place_and_link(
            "XGLOWCOLOR", controls.ColourPicker("'X' glow colour"), 0, 2
        )
        self._place_label("'X' inner colour", 0, 3)
        self._place_and_link(
            "XINNERCOLOR", controls.ColourPicker("'X' inner colour of 'X'"), 0, 4
        )

        self._place_label("Lip colour", 1, 0)
        self._place_and_link("LIPCOLOR", controls.ColourPicker("Lip color"), 1, 1)
        self._place_label("Lip glow", 1, 2)
        self._place_and_link("LIPGLOW", controls.ColourPicker("Lip glow"), 1, 3)
        self._place_label("'X' light colour", 1, 4)
        self._place_and_link(
            "XLIGHTCOLOR",
            controls.ColourPicker(
                "Color of the light on upper right of 'X'", alpha_selector=True
            ),
            1,
            5,
        )

        self._place_label("'X' logo X change", 2, 0)
        self._place_and_link(
            "XSKEWXLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'X' logo X change"
            ),
            2,
            1,
            columnspan=2,
        )
        self._place_label("'X' logo Y change", 2, 3)
        self._place_and_link(
            "YSKEWXLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'X' logo Y change"
            ),
            2,
            4,
            columnspan=2,
        )
        self._place_label("Custom 'X' logo", 3, 0)
        self._place_and_link(
            "CUSTOMX",
            controls.FileSelectorOrZero(
                file_select_window_title="Custom 'X' logo", mask=".x"
            ),
            3,
            1,
            columnspan=5,
        ) 
