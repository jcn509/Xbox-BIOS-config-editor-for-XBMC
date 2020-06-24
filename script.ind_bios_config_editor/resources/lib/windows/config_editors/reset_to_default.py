"""Window used to select controls that should have their fields reset to
default
"""
try:
    # typing not available on XBMC4Xbox
    from typing import Any, Callable, Tuple
except:
    pass
import os

import xbmcgui
import pyxbmct

from .. import controls


class ResetToDefault(pyxbmct.AddonDialogWindow):
    """Window used to select controls that should have their fields reset to
    default
    """
    def __new__(cls, tab_names, reset_callback=None, *args, **kwargs):
        return super(ResetToDefault, cls).__new__(cls, *args, **kwargs)

    def __init__(self, tab_names, reset_callback=None, *args, **kwargs):
        # type: (Tuple[str], Callable, Any, Any) -> None
        super(ResetToDefault, self).__init__("Reset To Default", *args, **kwargs)
        self._reset_callback = reset_callback
        num_rows = 3 + len(tab_names)
        height = num_rows * 60
        self.setGeometry(600, height, num_rows, 2)

        self._tabs_to_reset = set()
        self.placeControl(
            pyxbmct.Label("Tabs To Reset", alignment=pyxbmct.ALIGN_CENTER_Y), 0, 0
        )
        self._radio_buttons = []
        for row, tab in enumerate(tab_names, 1):
            radio_button = controls.RadioButton(tab)
            self._radio_buttons.append(radio_button)
            radio_button.set_value(False)
            self.placeControl(radio_button, row, 0, columnspan=2)
            self.connect(
                radio_button,
                lambda state, t=tab, r=radio_button: self._tab_radio_button_toggled(
                    state, t, r
                ),
            )
        all_tabs_button = controls.ButtonWithIcon("Select All", "done.png")
        self.placeControl(all_tabs_button, 0, 1)
        self.connect(all_tabs_button, self._select_all_clicked)

        ok_button = controls.ButtonWithIcon("Reset Tabs", "arrow_repeat.png")
        self.placeControl(ok_button, num_rows - 1, 0)
        self.connect(ok_button, self._ok_clicked)

        cancel_button = controls.ButtonWithIcon("Cancel", "close.png")
        self.placeControl(cancel_button, num_rows - 1, 1)
        self.connect(cancel_button, self.close)

        self.setFocus(all_tabs_button)
        self.autoNavigation()

        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def _select_all_clicked(self):
        # type: () -> None
        for button in self._radio_buttons:
            button.set_value(True)

    def _tab_radio_button_toggled(self, state, tab, radio_button):
        # type: (bool, str, controls.RadioButton) -> None
        if state:
            self._tabs_to_reset.add(tab)
        else:
            self._tabs_to_reset.discard(tab)

    def _ok_clicked(self):
        # type: () -> None
        dialog = xbmcgui.Dialog()
        confirm = dialog.yesno(
            "Are you sure?",
            "Are you sure you want to reset these tabs?",
            "This can't be undone!",
        )
        del dialog

        if confirm:
            if self._reset_callback:
                self._reset_callback(self._tabs_to_reset)
            self.close()
