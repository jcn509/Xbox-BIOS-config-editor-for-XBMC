import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class General(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(General, self).__init__(config, tab_viewer, 6)

    def _create_controls(self):
        self._place_label("Background colour", 0, 0, columnspan=2)
        self._place_and_link(
            "BGCOLOR", controls.ColourPicker("Background colour"), 0, 3,
            columnspan=2
        )
        self._place_and_link(
            "NOLIGHTEN",
            controls.RadioButton("Disable light in upper right corner"),
            1,
            0,
            columnspan=3,
        )
        self._place_and_link("TMS", controls.RadioButton("Show TMs"), 1, 3, columnspan=3)
       
