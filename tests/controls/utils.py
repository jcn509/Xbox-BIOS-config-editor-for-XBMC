"""Useful utilities used during testing"""
import pyxbmct


def create_window_place_control(control, width=800, height=500, rows=5, columns=5):
    window = pyxbmct.AddonFullWindow()
    window.setGeometry(width, height, rows, columns)
    window.placeControl(control, 0, 0)

    return window
