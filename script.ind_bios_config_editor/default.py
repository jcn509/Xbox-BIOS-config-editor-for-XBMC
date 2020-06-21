"""An iND-BiOS config editor addon for XBMC4XBOX"""
# pytype dislikes this import. Making resources a package caused strange pytest
# errors, so that isn't a solution.
# pytype: disable=import-error
from resources.lib.windows.config_editors import (
    IndBiosConfigEditor,
)
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
