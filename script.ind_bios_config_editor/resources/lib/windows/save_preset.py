import xbmcgui
import pyxbmct
from resources.lib import controls
import os

class SavePreset(pyxbmct.AddonDialogWindow):
    def __new__(cls, file_created_callback = None, default_filename = None,
                *args, **kwargs):
        return super(SavePreset, cls).__new__(cls, *args, **kwargs)
    
    def __init__(self, file_created_callback = None, default_filename = None,
                 *args, **kwargs):
        super(SavePreset, self).__init__("Save Flubber-X Preset", *args, **kwargs)
        if file_created_callback:
            self._file_created_callback = file_created_callback

        default_dir = "Select Directory"
        if default_filename:
            if os.path.isfile(default_filename):
                default_dir, default_filename = os.path.split(default_filename)
                if not default_dir:
                    default_dir = "Select Directory"
            else:
                if os.path.isdir(default_filename):
                    default_dir = default_filename
                    default_filename = "Filename"
        else:
            default_filename = "Filename"

        num_rows = 3
        height = num_rows * 60
        self.setGeometry(600, height, num_rows, 4)

        self.placeControl(pyxbmct.Label("Directory"), 0, 0)
        self._dir_input = controls.FileSelector(default = default_dir, update_label_on_select = True,
                 type = 3, heading = "Select Directory")
        self.placeControl(self._dir_input, 0, 1, columnspan = 3)

        self.placeControl(pyxbmct.Label("Filename"), 1, 0)
        self._filename_input = controls.FakeEdit(default = default_filename, heading = "Filename")
        self.placeControl(self._filename_input, 1, 1, columnspan = 3)

        ok_button = controls.ButtonWithIcon("Save Preset", "file_arrow_down.png")
        self.placeControl(ok_button, 2, 0, columnspan = 2)
        self.connect(ok_button, self._ok_clicked)

        cancel_button = controls.ButtonWithIcon("Cancel", "close.png")
        self.placeControl(cancel_button, 2, 2, columnspan = 2)
        self.connect(cancel_button, self.close)
        
        self.setFocus(ok_button)
        self.autoNavigation()

        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def _ok_clicked(self):
        directory = self._dir_input.get_value()
        if not os.path.isdir(directory):
            # Do something?
            return
        full_filename = os.path.join(directory,
                                     self._filename_input.get_current_value())
        if os.path.isfile(full_filename):
            dialog = xbmcgui.Dialog()
            overwrite = dialog.yesno("File already exists!",
                                     "This file already exists!",
                                     "Do you want to overwrite it?")
            del dialog
            if not overwrite:
                return

        if self._file_created_callback:
            self._file_created_callback(full_filename)

        self.close()
        
