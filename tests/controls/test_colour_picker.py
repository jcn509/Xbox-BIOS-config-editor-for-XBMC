"""Tests for :lib.control.ColourPicker:"""
import warnings

import pytest

from lib.controls import ColourPicker
from ..utils import create_window_place_control


def create_colour_picker(mocker, **kwargs):
    # Get a funny deprecation warning from somewhere inside PyXBMCt
    with warnings.catch_warnings(record=True):
        mocker.patch("pyxbmct.Button")
        mocker.patch("pyxbmct.Image")
        colour_picker = ColourPicker(**kwargs)

        # Somethings not working quite right with kodistubs
        # All methods from pyxbmc.Image are not inherited!
        # And so they have to be mocked here, weird but
        # not too big of a deal.
        icon = colour_picker.get_icon()
        icon.getPosition = mocker.Mock()
        icon.getPosition.return_value = (0, 0)
        icon._connectCallback = mocker.Mock()
        icon.setColorDiffuse = mocker.Mock()

        button = colour_picker.get_button()
        button.getPosition.return_value = (0, 0)
        button.setLabel = mocker.Mock()

        # Without this mocking gives us some funny errors
        # as the mocked function returns a function
        button._connectCallback.return_value = True
        icon._connectCallback.return_value = True

        return colour_picker


_TEST_PARAMS = (
    ("FFFFFFFF", "FFFFFFFF", True),
    ("000000", "000000", False),
    ("0xAAFFAA", "0xAAFFAA", True),
    ("0xAAAAFFBB", "0xAAAAFFBB", True),
    ("0xAAAAFFBB", "0xAAFFBB", False),
)


@pytest.mark.parametrize(
    "default_colour, colour_actually_used, alpha_selector", _TEST_PARAMS
)
def test_colour_picker_initial_colour(
    mocker, default_colour, colour_actually_used, alpha_selector
):
    """Ensure that the initial colour is set correctly
    
    The alpha component should be removed from the colour if it is present and
    alpha_selector is False
    """
    colour_picker = create_colour_picker(
        mocker, default_colour=default_colour, alpha_selector=alpha_selector
    )
    button = colour_picker.get_button()
    icon = colour_picker.get_icon()

    create_window_place_control(colour_picker)

    button.setLabel.assert_called_with(colour_actually_used)
    icon.setColorDiffuse.assert_called_with(colour_actually_used)

    assert colour_picker.get_value() == colour_actually_used, "colour set correctly"


@pytest.mark.parametrize(
    "colour_to_set, colour_actually_used, alpha_selector", _TEST_PARAMS
)
def test_colour_picker_set_colour(
    mocker, colour_to_set, colour_actually_used, alpha_selector
):
    colour_picker = create_colour_picker(mocker, alpha_selector=alpha_selector)
    button = colour_picker.get_button()
    icon = colour_picker.get_icon()

    create_window_place_control(colour_picker)
    colour_picker.set_value(colour_to_set)

    button.setLabel.assert_called_with(colour_actually_used)
    icon.setColorDiffuse.assert_called_with(colour_actually_used)

    assert colour_picker.get_value() == colour_actually_used, "colour set correctly"
