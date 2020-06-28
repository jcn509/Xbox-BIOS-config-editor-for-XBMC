import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class General(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(General, self).__init__(config, tab_viewer, 2)

    def _create_controls(self):
        
        self._place_and_link("SHOWFLUB", controls.RadioButton("Show flubber"), 0, 0)
        self._place_and_link("NOSOUND", controls.RadioButton("Disable Sound"), 0, 1)
        self._place_and_link("480P", controls.RadioButton("Play in 480P"), 1, 0)
        self._place_and_link("FASTANI", controls.RadioButton("Fast Animation"), 1, 1)
        self._place_label("Camera view", 2, 0)
        self._place_and_link(
            "CAMERAVIEW",
            controls.SelectBox([str(x) for x in range(-1, 16)], "-1", "Camera view"),
            2,
            1,
        )
        self._place_and_link(
            "IFILTER",
            controls.RadioButton("Enable Interlace Filter"),
            3,
            0,
            columnspan=2,
        )
        
