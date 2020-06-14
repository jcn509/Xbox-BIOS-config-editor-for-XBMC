from abc import ABCMeta, abstractmethod
import pyxbmct
from .. import controls


class AbstractTab(pyxbmct.Group):
    __metaclass__ = ABCMeta

    NUM_ROWS = 10

    def __new__(cls, config, num_columns=4, default_columnspan=1):
        # Group.__new__ is not responsible for setting number of rows/columns
        return super(AbstractTab, cls).__new__(cls, cls.NUM_ROWS, 0)

    def __init__(self, config, num_columns=4, default_columnspan=1):
        super(AbstractTab, self).__init__(self.NUM_ROWS, num_columns)
        self._config = config
        self._num_columns = num_columns
        self._default_columnspan = default_columnspan
        self._fields = {}
        self._value_changed_callback = None
        self._value_converter = self._create_value_converter()
        self._last_preset_filename = None

    def reset_to_default(self):
        defaults = self._config.defaults()
        for field in self._fields:
            value = defaults[field]
            self._config.set(field, value)
            self._set_control_value(field, value, False)

    def _value_changed(self, field, value, control):
        if self._value_changed_callback:
            self._value_changed_callback(field, value)
        self._config.set(field, value)

    def _connectCallback(self, callable, window):
        self._value_changed_callback = callable
        return False

    def _set_control_value(self, field, value, trigger_callback=True):
        control = self._fields[field]
        # self._config.set(field, value)
            
        control.set_value(value, trigger_callback=trigger_callback)

    def _update_last_preset_filename(self, last_preset_filename):
        self._last_preset_filename = last_preset_filename
        if self._load_preset_button:
            self._load_preset_button.set_value(last_preset_filename)

    def load_preset(self, filename):
        self._update_last_preset_filename(filename)
        self._config.load_preset(filename, self._fields)
        for field in self._fields:
            self._set_control_value(field, value)

    def save_preset(self, filename):
        self._update_last_preset_filename(filename)
        with open(filename, "w") as preset_file:
            self._config.write(preset_file)

    def _save_preset_button_pressed(self):
        # Windows imports tabs so this import is delayed until here to avoid circular import issues
        from ..windows import SavePreset

        save_preset_window = SavePreset(self.save_preset, self._last_preset_filename)
        save_preset_window.doModal()
        del save_preset_window

    def create_horizontal_rule(self, row):
        self.placeControl(
            controls.HorizontalRule(),
            row,
            0,
            columnspan=self._num_columns,
            pad_x=0,
            pad_y=0,
        )

    def _place_load_preset_button(self, row, column, columnspan=None, *args, **kwargs):
        self._load_preset_button = controls.FileSelector(
            default="Load Preset",
            update_label_on_select=False,
            heading="Load Preset",
            icon_pad_x=7,
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
            "Save Preset", "file_arrow_down.png", icon_pad_x=7
        )
        self.placeControl(
            save_preset_button, row, column, columnspan=columnspan, *args, **kwargs
        )
        self._window.connect(save_preset_button, self._save_preset_button_pressed)

    def _place_and_link(
        self,
        field,
        control,
        row,
        column,
        *args,
        **kwargs
    ):

        self._fields[field] = control

        callback = lambda value=None: self._value_changed(
            field, value, control
        )
        self._window.connect(control, callback)
        self.placeControl(control, row, column, *args, **kwargs)

        self._set_control_value(
            field, self._config.get(field), trigger_callback=False
        )

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
            # There seems to be a bug with right alignment in XBMC4XBOX?
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

    def create_horizontal_rule(self, row):
        self.placeControl(
            controls.HorizontalRule(),
            row,
            0,
            columnspan=self._num_columns,
            pad_x=0,
            pad_y=0,
        )

    @abstractmethod
    def _create_controls(self):
        pass

    @abstractmethod
    def _create_value_converter(self):
        pass

    def _placedCallback(self, window, *args, **kwargs):
        super(AbstractTab, self)._placedCallback(window, *args, **kwargs)
        self._window = window
        self._create_controls()
