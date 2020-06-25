import pyxbmct
from ... import controls
from .abstract_ind_bios_tab import AbstractIndBiosTab


class XScreen(AbstractIndBiosTab):
    def __init__(self, config):
        super(XScreen, self).__init__(config, 6)

    def _create_controls(self):

        # Misc
        self._place_load_preset_button(0, 0)
        self._place_save_preset_button(0, 1)
        self._place_label("Background colour", 0, 2)
        self._place_and_link(
            "BGCOLOR", controls.ColourPicker("Background colour"), 0, 3
        )
        self._place_and_link(
            "NOLIGHTEN",
            controls.RadioButton("Disable light in upper right corner"),
            0,
            4,
            columnspan=2,
        )
        self.create_horizontal_rule(0)

        # 'X' Logo
        self._place_and_link("SHOWXEN", controls.RadioButton("Show 'X'"), 1, 0)

        self._place_label("'X' glow colour", 1, 1)
        self._place_and_link(
            "XGLOWCOLOR", controls.ColourPicker("'X' glow colour"), 1, 2
        )
        self._place_label("'X' inner colour", 1, 3)
        self._place_and_link(
            "XINNERCOLOR", controls.ColourPicker("'X' inner colour of 'X'"), 1, 4
        )
        self._place_and_link("TMS", controls.RadioButton("Show TMs"), 1, 5)

        self._place_label("Lip colour", 2, 0)
        self._place_and_link("LIPCOLOR", controls.ColourPicker("Lip color"), 2, 1)
        self._place_label("Lip glow", 2, 2)
        self._place_and_link("LIPGLOW", controls.ColourPicker("Lip glow"), 2, 3)
        self._place_label("'X' light colour", 2, 4)
        self._place_and_link(
            "XLIGHTCOLOR",
            controls.ColourPicker(
                "Color of the light on upper right of 'X'", alpha_selector=True
            ),
            2,
            5,
        )

        self._place_label("'X' logo X change", 3, 0)
        self._place_and_link(
            "XSKEWXLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'X' logo X change"
            ),
            3,
            1,
            columnspan=2,
        )
        self._place_label("'X' logo Y change", 3, 3)
        self._place_and_link(
            "YSKEWXLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'X' logo Y change"
            ),
            3,
            4,
            columnspan=2,
        )
        self._place_label("Custom 'X' logo", 4, 0)
        self._place_and_link(
            "CUSTOMX",
            controls.FileSelectorOrZero(
                file_select_window_title="Custom 'X' logo", mask=".x"
            ),
            4,
            1,
            columnspan=5,
        )
        self.create_horizontal_rule(4)

        # 'XBOX' text
        self._place_and_link("IND3D", controls.RadioButton("iND 'XBOX' text"), 5, 0)
        self._place_label("'XBOX' text colour", 5, 1)
        self._place_and_link(
            "XBOXCOLOR", controls.ColourPicker("'XBOX' text colour"), 5, 2
        )
        self._place_label("Text Scale", 5, 3)
        self._place_and_link(
            "TEXTSCALE",
            controls.FakeSlider(
                min_value=0, max_value=100, keyboard_title="Text Scale"
            ),
            5,
            4,
            columnspan=2,
        )
        self._place_label("Custom 'XBOX' text", 6, 0)
        self._place_and_link(
            "CUSTOMTEXT",
            controls.FileSelectorOrZero(
                file_select_window_title="Custom 'XBOX' text", mask=".x"
            ),
            6,
            1,
            columnspan=5,
        )
        self.create_horizontal_rule(6)

        # 'MS' logo
        self._place_and_link("SHOWMSEN", controls.RadioButton("Show 'MS' logo"), 7, 0)
        self._place_and_link(
            "MSLOGOTRANSEN",
            controls.RadioButton("Use transperancy colour for 'MS' logo"),
            7,
            1,
            columnspan=2,
        )
        self._place_label("Transperancy colour", 7, 3)
        self._place_and_link(
            "MSLOGOTRANSCOLOR", controls.ColourPicker("Transperancy colour"), 7, 4
        )
        self._place_label("'MS' logo X change", 8, 0)
        self._place_and_link(
            "XSKEWLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'MS' logo X change"
            ),
            8,
            1,
            columnspan=2,
        )
        self._place_label("'MS' logo Y change", 8, 3)
        self._place_and_link(
            "YSKEWLOGO",
            controls.FakeSlider(
                min_value=-100, max_value=100, keyboard_title="'MS' logo Y change"
            ),
            8,
            4,
            columnspan=2,
        )
        self._place_label("Custom 'MS' logo", 9, 0)
        self._place_and_link(
            "CUSTOMLOGO",
            controls.FileSelectorOrZero(
                file_select_window_title="Custom 'MS' logo",
                mask=".bmp",
                use_thumbs=True,
            ),
            9,
            1,
            columnspan=5,
        )
        self.create_horizontal_rule(9)
