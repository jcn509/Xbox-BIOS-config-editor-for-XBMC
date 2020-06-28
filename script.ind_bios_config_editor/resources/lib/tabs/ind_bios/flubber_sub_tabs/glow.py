import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class Glow(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Glow, self).__init__(config, tab_viewer, 6)

    def _create_controls(self):
        # Glow
        self._place_label("Glow colour", 0, 0)
        self._place_and_link("GLOWCOLOR", controls.ColourPicker("Glow colour"), 0, 1)
        self._place_label("In/out glow colour", 1, 0)
        self._place_and_link(
            "IOGLOWCOLOR", controls.ColourPicker("Intro/outro glow colour"), 1, 1
        )        
