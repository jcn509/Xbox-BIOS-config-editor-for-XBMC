from resources.lib.windows import config_editors
import pyxbmct

# Enable or disable Estuary-based design explicitly
pyxbmct.skin.estuary = True

if __name__ == "__main__":
    window = config_editors.IndBiosConfigEditor("F:\\test_ind_bios.cfg")
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window
