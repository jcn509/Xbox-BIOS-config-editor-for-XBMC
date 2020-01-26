import pyxbmct
from ... import controls
from .abstract_ind_bios_tab import AbstractIndBiosTab


class Basic(AbstractIndBiosTab):
    def __init__(self, config):
        super(Basic, self).__init__(config, 8, default_columnspan=2)

    def _create_controls(self):
        self._place_label("In game reset mode", 0, 0)

        igr_modes = ["Off", "Compatible", "Quick"]
        self._place_and_link(
            "IGRMODE",
            controls.SelectBox(igr_modes, "Quick", title="In game reset mode"),
            0, 2,
            custom_control_to_config_converter=lambda value: str(igr_modes.index(value)),
            custom_config_to_control_converter=lambda value: igr_modes[int(value)]
        )
        self._place_and_link(
            "IGRLOADSDASH",
            controls.RadioButton("Load Dashboard on IGR"),
            1, 0,
            columnspan=4
        )
        self._place_and_link(
            "AUTOLOADDVD",
            controls.RadioButton("Autoload DVD (if DVD is in tray)"),
            2, 0,
            columnspan=4
        )
        self._place_and_link(
            "AVCHECK",
            controls.RadioButton("Check for AV Pack"),
            3, 0
        )
        self._place_and_link(
            "RESETONEJECT",
            controls.RadioButton("Reset on Eject"),
            3, 2
        )
        self._place_label("Fan speed", 4, 0, columnspan=1)
        self._place_and_link(
            "FANSPEED",
            controls.FakeSlider(min_value=10, max_value=50),
            4, 1,
            columnspan=3
        )
        self._place_and_link(
            "LEDPATTERN",
            controls.LedPattern(),
            0, 4,
            rowspan=5,
            columnspan=4,
            pad_x=0,
            pad_y=0
        )
