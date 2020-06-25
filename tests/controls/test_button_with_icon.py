"""Tests for controls.ButtonWithIcon"""
import warnings

import pytest
import pyxbmct

from lib.controls import ButtonWithIcon
import os
import sys
import math
import lib

def create_button_with_icon(mocker, **kwargs):
    # Get a funny deprecation warning from somewhere inside PyXBMCt 
    with warnings.catch_warnings(record=True):
        mocker.patch("pyxbmct.Button")
        mocker.patch("pyxbmct.Image")
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

def _create_window_place_control(control, width=800, height=500, rows=5, columns=5):
    window = pyxbmct.AddonFullWindow()
    window.setGeometry(width, height, rows, columns)
    window.placeControl(control, 0, 0)

    return window

def test_disable(button_with_icon):
    """Ensure that the button is disabled and the icon is made slightly transparent"""
    button = button_with_icon.get_button()
    icon = button_with_icon.get_icon()
    button_with_icon.setEnabled(False)
    button.setEnabled.assert_called_once_with(False)
    icon.setColorDiffuse.assert_called_once_with("0x5FFFFFFF")

def test_enable(button_with_icon):
    """Ensure that the button is enabled and the icon is made opaque"""
    button = button_with_icon.get_button()
    icon = button_with_icon.get_icon()
    button_with_icon.setEnabled(True)
    button.setEnabled.assert_called_once_with(True)
    icon.setColorDiffuse.assert_called_once_with("0xFFFFFFFF")

def test_connect(button_with_icon, mocker):
    """Ensure that connected callbacks are triggered when the button is clicked

    It is the button, not the 'button with icon' that users will actually click on    
    """
    window = _create_window_place_control(button_with_icon)
    mocker.spy(window, "connect")
    test_func = mocker.Mock()

    window.connect(button_with_icon, test_func)
    button = button_with_icon.get_button()
    icon = button_with_icon.get_icon()

    window.connect.assert_has_calls([
        mocker.call(button_with_icon, test_func),
        mocker.call(button, test_func),
    ])
    assert 2 == window.connect.call_count, "window.connect only called for button and button_with_icon"
    
    window.onControl(button)
    window.onControl(button_with_icon)
    test_func.assert_called()


@pytest.mark.parametrize(
    "button_x, button_width, icon_pad_x, icon_width, icon_height, expected_icon_x, icon_y",
    (
        (0, 400, 4, 40, 50, 356, 10),
        (0, 400, 4, 40, 50, 356, 10),
        (20, 400, 4, 40, 50, 376, 10),
        (0, 400, 4, 40, 50, 356, 54),
        (-10, 30, 5, 10, 90, 5, 12),
        (-10, 30, 5, 90, 10, -35, 12)
    ) 
)
def test_icon_position(mocker, button_x, button_width, icon_pad_x, icon_width, icon_height, expected_icon_x, icon_y):
    """Test that the icon ends up in the correct position.
    
    Its X value should be modified
    Its Y should be whatever is set by placeControl
    """
    button_with_icon = create_button_with_icon(mocker, icon_pad_x = icon_pad_x)

    button = button_with_icon.get_button()
    icon = button_with_icon.get_icon()
    icon.getWidth.return_value = icon_width
    icon.getHeight.return_value = icon_height

    # Icon X should not influence position
    # Icon Y should not be altered, it should be what is set by placeControl
    icon.getPosition.return_value = (-1000000, icon_y)

    button.getPosition.return_value = (button_x, 0)
    button.getWidth.return_value = button_width
    
    window = _create_window_place_control(button_with_icon)
    # Only care about the last call. First element of call is x coordinate
    icon.setPosition.assert_called_with(expected_icon_x, icon_y)
