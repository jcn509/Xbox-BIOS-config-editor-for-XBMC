import pyxbmct
from ... import controls
from .abstract_ind_bios_tab import AbstractIndBiosTab


class Flubber(AbstractIndBiosTab):
    def __init__(self, config):
        super(Flubber, self).__init__(config, 6)

    def _create_controls(self):
        self._place_load_preset_button(0, 0)
        self._place_save_preset_button(0, 1)
        # Glow
        self._place_label("Glow colour", 0, 2)
        self._place_and_link("GLOWCOLOR", controls.ColourPicker("Glow colour"), 0, 3)
        self._place_label("In/out glow colour", 0, 4)
        self._place_and_link(
            "IOGLOWCOLOR", controls.ColourPicker("Intro/outro glow colour"), 0, 5
        )
        self.create_horizontal_rule(0)

        # Fog
        self._place_and_link("FOGON", controls.RadioButton("Enable fog"), 1, 0)
        self._place_label("Fog 1 colour", 1, 1)
        self._place_and_link(
            "FOG1COLOR",
            controls.ColourPicker("Fog 1 colour", alpha_selector=True),
            1,
            2,
        )
        self._place_label("Fog 2 colour", 1, 3)
        self._place_and_link(
            "FOG2COLOR",
            controls.ColourPicker("Fog 2 colour", alpha_selector=True),
            1,
            4,
        )
        # Not sure what on earth this does??
        ##        self._place_and_link(
        ##            "FOG1ABS",
        ##            controls.RadioButton("Absolute colour, overides FOG1 colour"),
        ##            6, 2
        ##        )
        self.create_horizontal_rule(1)

        # Flubber
        self._place_and_link("SHOWFLUB", controls.RadioButton("Show flubber"), 2, 0)
        self._place_and_link("NOSOUND", controls.RadioButton("Disable Sound"), 2, 1)
        self._place_and_link("480P", controls.RadioButton("480P"), 2, 2)
        self._place_and_link("FASTANI", controls.RadioButton("Fast Animation"), 2, 3)
        self._place_label("Camera view", 2, 4)
        self._place_and_link(
            "CAMERAVIEW",
            controls.SelectBox(
                [str(x) for x in range(-1, 16)], "-1", "Camera view"
            ),
            2,
            5
        )
        self._place_and_link(
            "IFILTER",
            controls.RadioButton("Enable Interlace Filter"),
            3,
            0,
            columnspan=2,
        )
        self._place_label("Background colour", 3, 2)
        self._place_and_link(
            "BLOBBGC", controls.ColourPicker("Background colour"), 3, 3
        )
        self.create_horizontal_rule(3)

        # Blob
        self._place_and_link("BLOBSDEAD", controls.RadioButton("No blob"), 4, 0)
        self._place_and_link(
            "WIREFRAMEBLOB",
            controls.RadioButton("Show blob in wireframe"),
            4,
            1,
            columnspan=2,
        )
        self._place_and_link("BLOBTHROB", controls.RadioButton("Blob throb"), 4, 3)
        self._place_and_link("SLOWMOBLOB", controls.RadioButton("Slow Down Blob"), 4, 4)
        self._place_and_link("SPIKEYBLOB", controls.RadioButton("Spikey blob"), 4, 5)
        self._place_label("Blob colour", 5, 0)
        self._place_and_link("BLOBCOLOR", controls.ColourPicker("Blob olour"), 5, 1)
        self._place_label("Radi of the blob", 5, 2)
        self._place_and_link(
            "BLOBRADI",
            controls.FakeSlider(
                min_value=0, max_value=100, picker_title="Radi of the blob"
            ),
            5,
            3,
            columnspan=2,
        )

        self._place_label("Custom blob", 6, 0)
        self._place_and_link(
            "CUSTOMBLOB",
            controls.FileSelectorOrZero(heading="Custom blob", mask=".x"),
            6,
            1,
            columnspan=5,
        )
        self.create_horizontal_rule(6)

        # Scenery
        self._place_and_link(
            "NOFLUBBG",
            controls.RadioButton("Disable Flub BG (Disable Scenery)"),
            7,
            0,
            columnspan=2,
        )
        self._place_label("Scenery colour 1", 7, 2)
        self._place_and_link(
            "SCENECOLOR1",
            controls.ColourPicker("Scenery colour 1", alpha_selector=True),
            7,
            3,
        )
        self._place_label("Scenery colour 2", 7, 4)
        self._place_and_link(
            "SCENECOLOR2",
            controls.ColourPicker("Scenery colour 2", alpha_selector=True),
            7,
            5,
        )
        self._place_label("Scenery colour 3", 8, 0)
        self._place_and_link(
            "SCENECOLOR3",
            controls.ColourPicker("Scenery colour 3", alpha_selector=True),
            8,
            1,
        )
        self.create_horizontal_rule(8)
