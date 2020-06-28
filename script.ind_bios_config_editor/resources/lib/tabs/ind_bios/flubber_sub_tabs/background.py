import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class Background(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Background, self).__init__(config, tab_viewer, 4, default_columnspan=2)

    def _create_controls(self):
        self._place_and_link(
            "NOFLUBBG",
            controls.RadioButton("Disable Flub BG (Disable Scenery)"),
            0,
            0,
            columnspan=4
        )
        self._place_label("Scenery colour 1", 1, 0)
        self._place_and_link(
            "SCENECOLOR1",
            controls.ColourPicker("Scenery colour 1", alpha_selector=True),
            1,
            1,
        )
        self._place_label("Scenery colour 2", 2, 0)
        self._place_and_link(
            "SCENECOLOR2",
            controls.ColourPicker("Scenery colour 2", alpha_selector=True),
            2,
            1,
        )
        self._place_label("Scenery colour 3", 3, 0)
        self._place_and_link(
            "SCENECOLOR3",
            controls.ColourPicker("Scenery colour 3", alpha_selector=True),
            3,
            1,
        )
        self._place_label("Background colour", 4, 0, columnspan=1)
        self._place_and_link(
            "BLOBBGC", controls.ColourPicker("Background colour"), 4, 1,
            columnspan=3
        )
