import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class Fog(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Fog, self).__init__(config, tab_viewer, 6)

    def _create_controls(self): 
        self._place_and_link("FOGON", controls.RadioButton("Enable fog"), 0, 0, columnspan=2)
        self._place_label("Fog 1 colour", 1, 0)
        self._place_and_link(
            "FOG1COLOR",
            controls.ColourPicker("Fog 1 colour", alpha_selector=True),
            1,
            1,
        )
        self._place_label("Fog 2 colour", 2, 0)
        self._place_and_link(
            "FOG2COLOR",
            controls.ColourPicker("Fog 2 colour", alpha_selector=True),
            2,
            1,
        )
        # Not sure what on earth this does??
        ##        self._place_and_link(
        ##            "FOG1ABS",
        ##            controls.RadioButton("Absolute colour, overides FOG1 colour"),
        ##            6, 2
        ##        )
        
