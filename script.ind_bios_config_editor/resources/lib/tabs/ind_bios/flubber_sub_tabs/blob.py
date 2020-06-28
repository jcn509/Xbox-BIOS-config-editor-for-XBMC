import pyxbmct
from .... import controls
from ..abstract_ind_bios_tab import AbstractIndBiosTab


class Blob(AbstractIndBiosTab):
    def __init__(self, config, tab_viewer):
        super(Blob, self).__init__(config, tab_viewer, 5)

    def _create_controls(self):
        self._place_and_link("BLOBSDEAD", controls.RadioButton("No blob"), 0, 0)
        self._place_and_link(
            "WIREFRAMEBLOB",
            controls.RadioButton("Show blob in wireframe"),
            0,
            1,
        )
        self._place_and_link("BLOBTHROB", controls.RadioButton("Blob throb"), 0, 2)
        self._place_and_link("SLOWMOBLOB", controls.RadioButton("Slow down blob"), 0, 3)
        self._place_and_link("SPIKEYBLOB", controls.RadioButton("Spikey blob"), 0, 4)
        self._place_label("Blob colour", 1, 0)
        self._place_and_link("BLOBCOLOR", controls.ColourPicker("Blob colour"), 1, 1)
        self._place_label("Radi of the blob", 1, 2)
        self._place_and_link(
            "BLOBRADI",
            controls.FakeSlider(
                min_value=0, max_value=100, keyboard_title="Radi of the blob"
            ),
            2,
            2,
            columnspan=2,
        )

        self._place_label("Custom blob", 3, 0)
        self._place_and_link(
            "CUSTOMBLOB",
            controls.FileSelectorOrZero(
                file_select_window_title="Custom blob", mask=".x"
            ),
            3,
            1,
            columnspan=4,
        )

