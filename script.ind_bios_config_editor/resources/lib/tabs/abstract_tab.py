from abc import ABCMeta, abstractmethod
import pyxbmct
import xbmc
from .. import controls
from ..configs import ConfigError

class AbstractTab(pyxbmct.Group):
    __metaclass__ = ABCMeta

    NUM_ROWS = 7

    def __new__(cls, config, tab_viewer, num_columns=4, default_columnspan=1):
        # Group.__new__ is not responsible for setting number of rows/columns
        return super(AbstractTab, cls).__new__(cls, cls.NUM_ROWS, 0)

    def __init__(self, config, tab_viewer, num_columns=4, default_columnspan=1):
        super(AbstractTab, self).__init__(self.NUM_ROWS, num_columns)
        self._config = config
        self._num_columns = num_columns
        self._default_columnspan = default_columnspan
        self._fields = {}
        self._value_changed_callback = None
        self._last_preset_filename = None
        self._tab_viewer = tab_viewer

        self._sub_tab_viewer = None # No sub-tabs by default

    def reset_to_default(self):
        defaults = self._config.defaults()
        for field in self._fields:
            value = defaults[field]
            self._config.set(field, value)
            self._set_control_value(field, value, False)
         
        if self._sub_tab_viewer is not None:
            # Not ideal, but currently all sub-tabs must exist before they can
            # be reset
            self._ensure_all_subtabs_exist()
            for tab in self._sub_tab_viewer.Values():
                if tab is not None:
                    tab.reset_to_default()
    
    def _call_value_changed_callback_if_exists(self, field, value):
        if self._value_changed_callback:
            self._value_changed_callback(field, value)


    def _value_changed(self, field, value):
        self._call_value_changed_callback_if_exists(field, value)
        
        # In almost all cases the controls themselves stop the user from
        # entering invalid values. However, sometimes it is still possible
        try:
            self._config.set(field, value)
        except ConfigError as e:
            xbmc.executebuiltin("Notification(Error setting " + field + ", " + str(e) + ")")

            # Revert the change
            control = self._fields[field]
            control.set_value(self._config.get(field))

    def _connectCallback(self, callback, window):
        self._value_changed_callback = callback
        return False

    def _set_control_value(self, field, value, trigger_callback=True):
        control = self._fields[field]
        # self._config.set(field, value)

        control.set_value(value, trigger_callback=trigger_callback)

    def _update_last_preset_filename(self, last_preset_filename):
        self._last_preset_filename = last_preset_filename
        if self._load_preset_button:
            self._load_preset_button.set_value(last_preset_filename)
    
    def _ensure_all_subtabs_exist(self):
        if self._sub_tab_viewer is not None:
            current_tab = self._sub_tab_viewer.get_current_tab_name() 
            for tab_name, tab in self._sub_tab_viewer.get_tabs().iteritems():
                if tab is None:
                    # Forcibly create the tabs
                    self._sub_tab_viewer.switch_tab(tab_name)
            
            # May be further levels of nesting
            for tab in self._sub_tab_viewer.get_tabs().values():
                self._sub_tab_viewer._ensure_all_subtabs_exist()

            # Go back to the current tab so that the user doesn't notice
            self._sub_tab_viewer.switch_tab(current_tab) 
    
    def _update_all_control_values(self):
        for field in self._fields:
            self._set_control_value(field, self.config.get(field))
        
        if self._sub_tab_viewer is not None:
            # Kind of a pain, but need tabs to exist before they can be set
            self._ensure_all_subtabs_exist()
            for tab in self._sub_tab_viewer.Values():
                tab._update_all_control_values()


    def load_preset(self, filename):
        self._update_last_preset_filename(filename)
        with open(filename, "r") as preset_file:
            self._config.load_preset(preset_file, self._fields)
        self._update_all_control_values()                

    def _set_values_for_config(self, config):
        for field in self._fields:
            self._set_control_value(field, self.config.get(field))
        
        if self._sub_tab_viewer is not None:
            # Kind of a pain, but need tabs to exist before they can
            # be used in this process!
            self._ensure_all_subtabs_exist()
            for tab in self._sub_tab_viewer.get_tabs().values():
                tab._set_values_for_config(config)
    
    def _get_all_fields(self, config):
        sub_tab_fields = []
        if self._sub_tab_viewer is not None:
            self._ensure_all_subtabs_exist()
            [field for field in tab._get_all_fields() for tab in self._sub_tab_viewer.get_tabs().values()]

        return self._fields + sub_tab_fields

    def save_preset(self, filename): 
        self._update_last_preset_filename(filename)
        with open(filename, "w") as preset_file:
            self._config.save_preset(preset_file, self._get_all_fields())

    def _save_preset_button_pressed(self):
        # Windows imports tabs so this import is delayed until here to avoid circular import issues
        from ..windows import SavePreset

        save_preset_window = SavePreset(self.save_preset, self._last_preset_filename)
        save_preset_window.doModal()
        del save_preset_window

    def _place_load_preset_button(self, row, column, columnspan=None, *args, **kwargs):
        self._load_preset_button = controls.FileSelector(
            default_filename="Load Preset",
            update_label_on_select=False,
            file_select_window_title="Load Preset",
            custom_icon="file_arrow_up.png",
        )
        self.placeControl(
            self._load_preset_button,
            row,
            column,
            columnspan=columnspan,
            *args,
            **kwargs
        )
        self._window.connect(self._load_preset_button, self.load_preset)

    def _place_save_preset_button(self, row, column, columnspan=None, *args, **kwargs):
        save_preset_button = controls.ButtonWithIcon(
            "Save Preset", "file_arrow_down.png"
        )
        self.placeControl(
            save_preset_button, row, column, columnspan=columnspan, *args, **kwargs
        )
        self._window.connect(save_preset_button, self._save_preset_button_pressed)

    def _place_and_link(self, field, control, row, column, *args, **kwargs):

        self._fields[field] = control

        callback = lambda value=None: self._value_changed(field, value)
        self._window.connect(control, callback)
        self.placeControl(control, row, column, *args, **kwargs)

        self._set_control_value(field, self._config.get(field), trigger_callback=False)

    def _place_label(
        self,
        text,
        row,
        column,
        alignment=pyxbmct.ALIGN_RIGHT | pyxbmct.ALIGN_CENTER_Y,
        rowspan=1,
        columnspan=None,
        pad_x=5,
        pad_y=5,
        *args,
        **kwargs
    ):
        if alignment & pyxbmct.ALIGN_RIGHT:
            if columnspan is None:
                columnspan = self._default_columnspan
            # There seems to be a bug with right alignment in XBMC4Xbox?
            # Or maybe it is deliberate?
            column += columnspan

        label = pyxbmct.Label(text, alignment=alignment, *args, **kwargs)
        self.placeControl(label, row, column, rowspan, columnspan, -pad_x, pad_y)

    def placeControl(
        self, control, row, column, rowspan=1, columnspan=None, pad_x=5, pad_y=5
    ):
        if columnspan == None:
            columnspan = self._default_columnspan
        super(AbstractTab, self).placeControl(
            control, row, column, rowspan, columnspan, pad_x, pad_y
        )

    @abstractmethod
    def _create_controls(self):
        pass

    def _placedCallback(self, window, *args, **kwargs):
        super(AbstractTab, self)._placedCallback(window, *args, **kwargs)
        self._window = window
        self._create_controls()
