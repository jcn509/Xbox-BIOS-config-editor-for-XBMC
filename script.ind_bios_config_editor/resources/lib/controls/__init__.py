"""All basic controls that have some state (i.e. not buttons) are a part of
this package.

Some controls implement new functionality that is not available by default in
XBMC whilst others are simply wrappers for existing controls.

All controls have the same basic interface. Unlike the default controls from
PyXBMCt/XBMC which all have different methods that are used to set/get their
values. (This does not apply to buttons as they do not have a value to get or
set.). This was done to loosen the coupling between the control classes and the
classes that use them.

All controls also pass their current value to whatever callback is connected to
them via window.connect. (Unlike those defined in PyXBMCt.)
"""

from .colour_picker import ColourPicker
from .colour_picker_full import ColourPickerFull
from .file_selector import *
from .file_selector_or_zero import *
from .select_box import *
from .fake_slider import *
from .fake_edit import *
from .led_pattern import *
from .horizontal_rule import *
from .button_with_icon import *
from .radio_button import *
from .abstract_control import *
