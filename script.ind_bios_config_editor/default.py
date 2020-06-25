"""An iND-BiOS config editor addon for XBMC4XBOX"""
# pytype dislikes this import. Making resources a package caused strange pytest
# errors, so that isn't a solution.
# pytype: disable=import-error

import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resources"))

from lib.windows.config_editors import IndBiosConfigEditor

# pytype: enable=import-error
import pyxbmct

# Enable or disable Estuary-based design explicitly
pyxbmct.skin.estuary = True

if __name__ == "__main__":
    window = IndBiosConfigEditor("F:\\test_ind_bios.cfg")
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window
