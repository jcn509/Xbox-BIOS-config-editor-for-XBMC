"""Tests for :lib.image_utils:"""
import os

import pytest

from lib.image_utils import get_png_aspect_ratio, get_png_dimensions

_TEST_DATA = (
    ("vine.png", 640, 320),
    ("dove.png", 522, 640),
    ("santa.png", 640, 451)
)

_TEST_DATA_INVALID = (
    "actually_a_jpg.png",
    "insect.jpg"
)

def get_full_file_path(file_path):
    return os.sep.join((os.path.dirname(os.path.realpath(__file__)), "test_images", file_path))

@pytest.mark.parametrize(
    "filename, width, height",
    _TEST_DATA
)
def test_get_png_dimensions(mocker, filename, width, height):
    """Tests :lib.image_utils.get_png_dimensions:"""
    file_path = get_full_file_path(filename)
    assert get_png_dimensions(file_path) == (width, height)

@pytest.mark.parametrize(
    "filename",
    _TEST_DATA
)
def test_get_png_dimensions_not_a_png(filename):
    """Ensures that :lib.image_utils.get_png_dimensions: raises an exception
    when the image it is given is not a PNG
    """
    with pytest.raises(Exception):
        get_png_dimensions(filename)

@pytest.mark.parametrize(
    "filename",
    _TEST_DATA
)
def test_get_png_aspect_ratio_not_a_png(filename):
    """Ensures that :lib.image_utils.get_png_aspect_ratio: raises an exception
    when the image it is given is not a PNG
    """
    with pytest.raises(Exception):
        get_png_aspect_ratio(filename)

@pytest.mark.parametrize(
    "filename, width, height",
    _TEST_DATA
)
def test_get_png_aspect_ratio_unit_test(mocker, filename, width, height):
    """Tests :lib.image_utils.get_png_aspect_ratio:
    
    mocks :lib.image_utils.get_png_aspect_ratio:
    """
    file_path = get_full_file_path(filename)
    mocker.patch("lib.image_utils.get_png_dimensions", return_value = (width, height))
    assert get_png_aspect_ratio(file_path) == (float(width) / height)


@pytest.mark.parametrize(
    "filename, width, height",
    _TEST_DATA
)
def test_get_png_aspect_ratio_integration_test(mocker, filename, width, height):
    """Tests :lib.image_utils.get_png_aspect_ratio:
    
    Does not mock :lib.image_utils.get_png_aspect_ratio:
    """
    file_path = get_full_file_path(filename)
    assert get_png_aspect_ratio(file_path) == (float(width) / height)

