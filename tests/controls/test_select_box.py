"""Tests for :lib.controls.SelectBox:"""

from types import MethodType
import warnings

import pytest

from lib.controls import SelectBox


def _create_select_box(mocker, options, **kwargs):
    # Get a funny deprecation warning from somewhere inside PyXBMCt 
    with warnings.catch_warnings(record=True):
        mocker.patch("pyxbmct.Image")
        mocker.patch("pyxbmct.Button")
        
        select_box = SelectBox(options, **kwargs)
        
        # Have to mock the getting and setting of the label...
        button = select_box.get_button()
        button._label_for_test = None
        
        def getLabel(self):
            return self._label_for_test
        button.getLabel = MethodType(getLabel, button)

        def setLabel(self, value):
            self._label_for_test = value
        button.setLabel = MethodType(setLabel, button)
        button.setLabel = mocker.spy(button, "setLabel")
         
        return select_box

@pytest.mark.parametrize(
    "options",
    (
        ("one", "two"),
        ["one", "two"],
        ("asdasd",),
        ["asdasd", "azsdsad"]
    ) 
)
def test_create_with_valid_options(mocker, options):
    """Ensure that a select box can be created with valid options"""
    _create_select_box(mocker, options)

@pytest.mark.parametrize(
    "options, expected_exception",
    (
        ("one option", TypeError),
        ([12, "232"], TypeError),
        (("one", 2), TypeError),
        ([], ValueError),
        (tuple(), ValueError),
        ({"test": "test"}, TypeError)
    )
)
def test_create_with_invalid_options(mocker, options, expected_exception):
    """Ensure that a select box cannot be created with an invalid set of
    options and that a ValueError is thrown
    """
    with pytest.raises(expected_exception):
        _create_select_box(mocker, options)

@pytest.mark.parametrize(
    "options, option_to_set",
    (
        (("one", "two"), "one"),
        (["one", "two"], "two"),
        (("asdasd", ), "asdasd"),
    ) 
)
def test_set_valid_option(mocker, options, option_to_set):
    """Ensure that a select box can have its value set to a valid option"""
    select_box = _create_select_box(mocker, options)
    select_box.set_value(option_to_set)

    button = select_box.get_button()
    button.setLabel.assert_called_with(option_to_set)

    assert select_box.get_value() == option_to_set

@pytest.mark.parametrize(
    "options, option_to_set",
    (
        (("one", "two"), "One"),
        (["one", "two"], "three"),
        (("asdasd", ), "a"),
    ) 
)
def test_set_invalid_option(mocker, options, option_to_set):
    """Ensure that a select box cannot have its value set to an invalid option
    and that a ValueError is thrown
    """
    select_box = _create_select_box(mocker, options)
    
    with pytest.raises(ValueError):
        select_box.set_value(option_to_set)

    button = select_box.get_button()
    button.setLabel.assert_not_called()

    assert select_box.get_value() != option_to_set, "option not actually set"
