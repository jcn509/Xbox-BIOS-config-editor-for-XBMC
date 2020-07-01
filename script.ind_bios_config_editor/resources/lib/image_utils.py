"""Utilities for checking if an image is a PNG and calculating its height and
aspect ratio
"""
import struct

def _is_png(data):
    return (data[:8] == '\211PNG\r\n\032\n'and (data[12:16] == 'IHDR'))

def get_png_dimensions(filename):
    """PIL not available so this is a modified version of:
    https://stackoverflow.com/questions/8032642/how-to-obtain-image-size-using-standard-python-class-without-using-external-lib
    """
    # type: (str) -> Tuple[int, int]
    with open(filename, "rb") as image_file:
        data = image_file.read(25)
    if _is_png(data):
        w, h = struct.unpack('>LL', data[16:24])
        width = int(w)
        height = int(h)
    else:
        raise Exception('not a png image')
    return width, height

def get_png_aspect_ratio(filename):
    """:returns: the aspect ratio (width/height) for a PNG"""
    # type: (str) -> float
    width, height = get_png_dimensions(filename)
    return float(width) / height

