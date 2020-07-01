"""Tests for :lib.tabs.TabViewer:"""

from collections import OrderedDict
import warnings
from types import MethodType

import pytest
from pyxbmct import Button

from lib.tabs import TabViewer
from lib.configs import IndBiosConfig
from lib.controls import ButtonWithIcon
from lib.tabs.ind_bios import Basic, Boot
from ..utils import create_window_place_control

def _create_tab_viewer(mocker, config, tabs, **kwargs):
    """Create the tab viewer instance"""
    with warnings.catch_warnings(record=True):
        mocker.patch("pyxbmct.Group")
        mocker.patch("pyxbmct.Button")
        mocker.patch.object(Button, "setEnabled", autospec=True)
        mocker.patch("pyxbmct.Image")
            
        return TabViewer(config, 4, 1, tabs, **kwargs)

@pytest.fixture()
def tabs_dict(mocker):
    # patches for the sake of creating tabs
    mocker.patch("pyxbmct.Label")
    mocker.patch("pyxbmct.RadioButton")
    
    mocker.patch("lib.controls.ButtonWithIcon")
    mocker.patch("lib.controls.FakeEdit")
    mocker.patch("lib.controls.FileSelector")
    mocker.patch("lib.controls.FakeSlider")
    mocker.patch("lib.controls.RadioButton")
    mocker.patch("lib.controls.SelectBox")

    tabs = OrderedDict((("Basic", Basic), ("Boot settings", Boot)))
    for tab in tabs.values():
        tab.setEnabled = mocker.Mock()
        tab.setVisible = mocker.Mock()
    return tabs

@pytest.fixture()
def config(mocker):
    return IndBiosConfig()

@pytest.mark.parametrize(
    "tab_icons",
    (
        None,
        {
            "Basic": "test.png"
        }
    )
)
def test_create_and_place(config, tabs_dict, mocker, tab_icons):
    """Ensure that when the viewer is created only the first tab is visible"""
    tab_viewer = _create_tab_viewer(mocker, config, tabs_dict, tab_icons=tab_icons)
    
    create_window_place_control(tab_viewer)
    assert isinstance(tabs_dict["Basic"], Basic), "Basic tab was created"
    assert isinstance(tabs_dict["Boot settings"], type), "Boot settings tab not created"
    assert not isinstance(tabs_dict["Boot settings"], Boot), "Boot settings tab not created"
    

@pytest.mark.parametrize(
    "tab_icons",
    (
        None,
        {
            "Basic": "test.png"
        }
    )
)
def test_switch_tab(config, tabs_dict, mocker, tab_icons):
    """Tests a basic flow where the tab is changed to one that has not been
    opened before and then switched back. Ensures that tabs are created
    enabled/disabled and shown/hidden as they should be
    """
    tab_viewer = _create_tab_viewer(mocker, config, tabs_dict, tab_icons=tab_icons)
    
    create_window_place_control(tab_viewer)

    tab_viewer.switch_tab("Boot settings")
 
    assert isinstance(tabs_dict["Boot settings"], Boot), "Boot settings tab created"
    tabs_dict["Basic"].setEnabled.assert_called_with(False)
    tabs_dict["Basic"].setVisible.assert_called_with(False)
   
    # Not been called as just created so no need
    tabs_dict["Boot settings"].setEnabled.assert_not_called()
    tabs_dict["Boot settings"].setVisible.assert_not_called()
    
    tab_viewer.switch_tab("Basic")
    tabs_dict["Basic"].setEnabled.assert_called_with(True)
    tabs_dict["Basic"].setVisible.assert_called_with(True)
   
    # Should be called this time as this tab needs to be hidden
    tabs_dict["Boot settings"].setEnabled.assert_called_with(False)
    tabs_dict["Boot settings"].setVisible.assert_called_with(False)
    


