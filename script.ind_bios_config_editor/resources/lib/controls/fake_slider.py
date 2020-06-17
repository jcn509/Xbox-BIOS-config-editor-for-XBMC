import pyxbmct
import xbmcgui
import os
from .abstract_control import AbstractControl


class FakeSlider(AbstractControl, pyxbmct.Group):
    """
        FakeSlider(textureback=None, texture=None, texturefocus=None, orientation=xbmcgui.HORIZONTAL)
        
        Not a derivate of ControlSlider class.
        
        Implements a movable slider for adjusting some value.
        
        :param textureback: string -- image filename.
        :param texture: string -- image filename.
        :param texturefocus: string -- image filename.
        
        .. note:: After you create the control, you need to add it to the window with placeControl().
        
        Example::
        
            self.slider = FakeSlider()
        """

    def __new__(
        cls,
        min_value=0,
        max_value=255,
        default_value=None,
        step=1,
        click_to_type_value=True,
        picker_title="Enter Number",
        show_value_label=True,
        value_label_width=1,
        total_width=4,
        textureback=None,
        texture=None,
        texturefocus=None,
        *args,
        **kwargs
    ):
        return super(FakeSlider, cls).__new__(cls, 1, 1, *args, **kwargs)

    def __init__(
        self,
        min_value=0,
        max_value=255,
        default_value=None,
        step=1,
        click_to_type_value=True,
        picker_title="Enter Number",
        show_value_label=True,
        value_label_width=1,
        total_width=4,
        textureback=None,
        texture=None,
        texturefocus=None,
        *args,
        **kwargs
    ):
        super(FakeSlider, self).__init__(1, total_width, *args, **kwargs)

        if max_value < min_value:
            raise ValueError("max_value must be >= min_value")
        if default_value == None:
            default_value = min_value
        if default_value > max_value:
            raise ValueError("default_value must be <= max_value")
        if default_value < min_value:
            raise ValueError("default_value must be >= min_value")

        self._outline_texture = (
            textureback
            if textureback
            else os.path.join(pyxbmct.skin.images, "Slider", "osd_slider_bg.png")
        )
        self._nib_texture_not_focussed = (
            texture
            if texture
            else os.path.join(pyxbmct.skin.images, "Slider", "osd_slider_nibNF.png")
        )
        self._nib_texture_focussed = (
            texturefocus
            if texturefocus
            else os.path.join(pyxbmct.skin.images, "Slider", "osd_slider_nib.png")
        )

        # if xbmc.getInfoLabel('System.BuildVersion')[:2] >= '17':
        #    kwargs['orientation'] = xbmcgui.HORIZONTAL

        self._value_changed_callback = None
        self._step = step
        self._min_value = min_value
        self._max_value = max_value
        self._default_value = default_value

        self._picker_title = picker_title
        self._click_to_type_value = click_to_type_value

        self._show_value_label = show_value_label
        self._value_label_width = value_label_width
        self._total_width = total_width

    def get_value(self):
        return self._value

    def _add_to_value_if_focussed(self, num_to_add):
        if self._window.getFocus() == self._nib:
            self.set_value(self._value + num_to_add)

    def _increase_if_focussed(self):
        self._add_to_value_if_focussed(self._step)

    def _decrease_if_focussed(self):
        self._add_to_value_if_focussed(-self._step)

    def set_value(self, value, trigger_callback=True):
        if value < self._min_value:
            value = self._min_value
        elif value > self._max_value:
            value = self._max_value

        self._value = value
        nib_x = int(
            round(self._nib_min_x + (float(value - self._min_value) * self._nib_x_unit))
        )

        self._nib.setPosition(nib_x, self._nib_y)

        if self._show_value_label:
            self._value_label.setLabel(str(value))

        if trigger_callback and self._value_changed_callback:
            self._value_changed_callback(value)

    def _pick_value(self):
        dialog = xbmcgui.Dialog()
        self.set_value(
            int(dialog.numeric(0, self._picker_title, str(self.get_value())))
        )

        # I believe these aren't garbage collected?
        del dialog

    def _connectCallback(self, callable, window):
        self._value_changed_callback = callable
        return False

    def _placedCallback(self, window, *args, **kwargs):
        super(FakeSlider, self)._placedCallback(window, *args, **kwargs)

        if self._show_value_label:
            slider_width = self._total_width - self._value_label_width
            label_text_align = pyxbmct.ALIGN_CENTER_Y
            self._value_label = pyxbmct.Label("", alignment=label_text_align)
            label_column = self._total_width - self._value_label_width
            self.placeControl(
                self._value_label,
                0,
                label_column,
                columnspan=self._value_label_width,
                pad_x=10,
                pad_y=0,
            )
        else:
            slider_width = self._total_width

        self._window = window
        width = int(
            round(
                float(self.getWidth())
                * (float(slider_width) / float(self._total_width))
            )
        )
        height = self.getHeight()
        x, y = self.getPosition()

        nib_pad = 0
        nib_size = min(width, height) - (2 * nib_pad)

        self._nib_min_x = float(x)  # Need a float later
        self._nib_y = y + (height / 2) - (nib_size / 2)
        self._nib_x_unit = float(width - nib_size) / float(
            self._max_value - self._min_value
        )

        self._nib = pyxbmct.Button(
            "",
            focusTexture=self._nib_texture_not_focussed,
            noFocusTexture=self._nib_texture_focussed,
        )
        self._nib.setWidth(nib_size)
        self._nib.setHeight(nib_size)

        # This is a bodge to ensure that window.autoNavigation works
        # properly for controls above or below the slider.
        # nib should never be accessed from the outside anyway...
        self._nib.getWidth = lambda: width
        self._nib.getHeight = lambda: height
        self._nib.getPosition = lambda: (x, y)

        self.addControl(self._nib)

        self.set_value(self._default_value, False)

        if self._click_to_type_value:
            window.connect(self._nib, self._pick_value)

        # Stop window.autoNavigation from allowing one to move
        # From this control to one on the left or right
        self._nib.controlLeft = lambda x: None
        self._nib.controlRight = lambda x: None
        window.connectEventList(
            [pyxbmct.ACTION_MOVE_RIGHT, pyxbmct.ACTION_MOUSE_WHEEL_UP],
            self._increase_if_focussed,
        )
        window.connectEventList(
            [pyxbmct.ACTION_MOVE_LEFT, pyxbmct.ACTION_MOUSE_WHEEL_DOWN],
            self._decrease_if_focussed,
        )

        outline = pyxbmct.Image(self._outline_texture)
        self.placeControl(outline, 0, 0, columnspan=slider_width, pad_x=0, pad_y=0)

    def _removedCallback(self, window):
        window.disconnectEventList(
            [pyxbmct.ACTION_MOVE_RIGHT, pyxbmct.ACTION_MOUSE_WHEEL_UP],
            self._increase_if_focussed,
        )
        window.disconnectEventList(
            [pyxbmct.ACTION_MOVE_LEFT, pyxbmct.ACTION_MOUSE_WHEEL_DOWN],
            self._decrease_if_focussed,
        )
