"""Tests for :lib.control.ColourPickerFull:"""
import warnings

import pytest

from lib.controls import ColourPickerFull, FakeSlider
from .utils import create_window_place_control

def create_colour_picker(mocker, **kwargs):
    # Get a funny deprecation warning from somewhere inside PyXBMCt 
    with warnings.catch_warnings(record=True):
        mocker.patch("pyxbmct.Button")
        mocker.patch("pyxbmct.Image")
        mocker.patch("pyxbmct.Label")
        mocker.patch("lib.controls.FakeSlider")
        FakeSlider.getPosition = mocker.Mock(return_value = (0,0))
        colour_picker = ColourPickerFull(**kwargs)
       
        return colour_picker

_TEST_PARAMS = (
    ("FFFFFFFF", "FFFFFFFF", True),
    ("000000", "000000", False),
    ("0xAAAAFFBB", "0xAAAAFFBB", True),
    ("0xAAAAFFBB", "0xAAFFBB", False),
)

@pytest.mark.parametrize(
    "default_colour, colour_actually_used, alpha_selector",
    _TEST_PARAMS
)
def test_colour_picker_initial_colour(mocker, default_colour, colour_actually_used, alpha_selector):
    """Ensure that the initial colour is set correctly
    
    The alpha component should be removed from the colour if it is present and
    alpha_selector is False
    """
    colour_picker = create_colour_picker(mocker, default_colour = default_colour, alpha_selector = alpha_selector) 
    create_window_place_control(colour_picker)
    
    assert colour_picker.get_value() == colour_actually_used, "colour set correctly"

@pytest.mark.parametrize(
    "colour_to_set, colour_actually_used, alpha_selector",
    _TEST_PARAMS
)
def test_colour_picker_set_colour(mocker, colour_to_set, colour_actually_used, alpha_selector):
    colour_picker = create_colour_picker(mocker, alpha_selector = alpha_selector)
    create_window_place_control(colour_picker)
    
    if colour_picker.get_value().startswith("0x") and not colour_to_set.startswith("0x"):
        colour_actually_used = "0x" + colour_actually_used
    elif not colour_picker.get_value().startswith("0x") and colour_to_set.startswith("0x"):
        colour_actually_used = colour_actually_used[2:]

    colour_picker.set_value(colour_to_set)

    assert colour_picker.get_value() == colour_actually_used, "colour set correctly"

