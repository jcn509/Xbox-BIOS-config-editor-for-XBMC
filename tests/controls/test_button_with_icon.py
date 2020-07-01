"""Tests for controls.ButtonWithIcon"""
import math
import lib
import os
import sys
import warnings

import pytest
import pyxbmct

from lib.controls import ButtonWithIcon
from .utils import create_window_place_control


def create_button_with_icon(mocker, image_width=1, image_height=1, **kwargs):
    # Get a funny deprecation warning from somewhere inside PyXBMCt
    with warnings.catch_warnings(record=True):
        mocker.patch("pyxbmct.Button")
        mocker.patch("pyxbmct.Image")
        mocker.patch("lib.controls.button_with_icon.get_png_aspect_ratio", return_value=float(image_width)/image_height) 
        
        button_with_icon = ButtonWithIcon("test text", "test.png", **kwargs)

        icon = button_with_icon.get_icon()
        icon.getPosition.return_value = (0, 0)

        button = button_with_icon.get_button()
        button.getPosition.return_value = (0, 0)

        # Without this mocking gives us some funny errors
        # as the mocked function returns a function
        button._connectCallback.return_value = True
        icon._connectCallback.return_value = True

        return button_with_icon


@pytest.fixture()
def button_with_icon(mocker):
    return create_button_with_icon(mocker)


@pytest.mark.parametrize(
    "enable, set_icon_colour_diffuse_on_set_enabled, expected_colour_diffuse",
    (
        (False, False, None),
        (False, True, "0x5FFFFFFF"),
        (True, False, None),
        (True, True, "0xFFFFFFFF"),
    ),
)
def test_set_enable(
    mocker, enable, set_icon_colour_diffuse_on_set_enabled, expected_colour_diffuse
):
    """Ensure that the button is correctly enabled or disabled and the icons
    opacity is adjusted appropriately
    """
    button_with_icon = create_button_with_icon(
        mocker,
        set_icon_colour_diffuse_on_set_enabled=set_icon_colour_diffuse_on_set_enabled,
    )
    button_with_icon.setEnabled(enable)

    button = button_with_icon.get_button()
    button.setEnabled.assert_called_once_with(enable)

    icon = button_with_icon.get_icon()
    if expected_colour_diffuse is None:
        icon.setColorDiffuse.assert_not_called()
    else:
        icon.setColorDiffuse.assert_called_once_with(expected_colour_diffuse)


def test_connect(button_with_icon, mocker):
    """Ensure that connected callbacks are triggered when the button is clicked

    It is the button, not the 'button with icon' that users will actually click on    
    """
    window = create_window_place_control(button_with_icon)
    mocker.spy(window, "connect")
    test_func = mocker.Mock()

    window.connect(button_with_icon, test_func)
    button = button_with_icon.get_button()
    icon = button_with_icon.get_icon()

    window.connect.assert_has_calls(
        [mocker.call(button_with_icon, test_func), mocker.call(button, test_func),]
    )
    assert (
        2 == window.connect.call_count
    ), "window.connect only called for button and button_with_icon"

    window.onControl(button)
    window.onControl(button_with_icon)
    test_func.assert_called()


@pytest.mark.parametrize(
    "button_x, button_y, button_width, button_height, icon_scale, image_width, image_height, expected_icon_x, expected_icon_y",
    (
        (0, 0, 400, 4, 50, 50, 40, 396, 1),
        (0, 20, 400, 4, 50, 50, 40, 396, 21),
        (100, 20, 400, 4, 50, 50, 40, 496, 21),

        (20, -5, 400, 4, 100, 60, 50, 415, -5),
        (20, -5, 400, 4, 50, 60, 50, 417, -4),
        
        (0, 12, 400, 40, 10, 100, 50, 374, 30),    
        (-15, 12, 400, 40, 10, 100, 50, 359, 30),    
    ),
)
def test_icon_position(
    mocker,
    button_x,
    button_y,
    button_width,
    button_height,
    icon_scale,
    image_width,
    image_height,
    expected_icon_x,
    expected_icon_y,
):
    """Test that the icon ends up in the correct position"""

    button_with_icon = create_button_with_icon(mocker, image_width = image_width, image_height = image_height, icon_scale=icon_scale)
    button = button_with_icon.get_button()
    icon = button_with_icon.get_icon()
    icon.getWidth.return_value = image_width
    icon.getHeight.return_value = image_height

    button.getPosition.return_value = (button_x, button_y)
    button.getWidth.return_value = button_width
    button.getHeight.return_value = button_height

    window = create_window_place_control(button_with_icon)
    # Only care about the last call. First element of call is x coordinate
    icon.setPosition.assert_called_with(expected_icon_x, expected_icon_y)

@pytest.mark.parametrize(
    "button_height, icon_scale, image_width, image_height, expected_image_width, expected_image_height",
    (
        (4, 50, 50, 40, 3, 2),

        (4, 100, 60, 50, 5, 4),
        (40, 50, 60, 50, 24, 20),
        
        (40, 10, 100, 50, 8, 4),    
    ),
)
def test_icon_dimenstions(
    mocker, button_height, icon_scale, image_width, image_height, expected_image_width, expected_image_height
):
    """Test that the icon ends up the correct size"""

    button_with_icon = create_button_with_icon(mocker, image_width = image_width, image_height = image_height, icon_scale=icon_scale)
    button = button_with_icon.get_button()
    icon = button_with_icon.get_icon()
    icon.getWidth.return_value = image_width
    icon.getHeight.return_value = image_height

    button.getHeight.return_value = button_height

    window = create_window_place_control(button_with_icon)
    # Only care about the last call. First element of call is x coordinate
    icon.setWidth.assert_called_with(expected_image_width)
    icon.setHeight.assert_called_with(expected_image_height)
