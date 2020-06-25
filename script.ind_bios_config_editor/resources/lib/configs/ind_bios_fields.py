"""Contains descriptions of all the fields in the iND-BiOS config in a named
tuple
"""

from collections import namedtuple

from .config_field import (
    BooleanField,
    IntegerField,
    DiscreteField,
    StringField,
    HDDFilePathField,
    OptionalHDDFilePathField,
    DVDFilePathField,
    HexColourField,
)

# Not what is accessible outside of this function, see IND_BIOS_FIELDS below
_IND_BIOS_FIELDS = {
    "autoloaddvd": BooleanField("AUTOLOADDVD", True),
    "avcheck": BooleanField("AVCHECK", True),
    "igrloadsdash": BooleanField("IGRLOADSDASH", False),
    "igrmode": DiscreteField("IGRMODE", "Quick", ("Off", "Compatible", "Quick")),
    "resetoneject": BooleanField("RESETONEJECT", False),
    "fanspeed": IntegerField("FANSPEED", 10, 10, 50),
    "ledpattern": StringField("LEDPATTERN", "GGGG", r"^[GROBN]{4}$"),
    "useallmemory": BooleanField("USEALLMEMORY", False),
    "macaddr": StringField(
        "MACADDR", "00:00:00:00:00:00", r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"
    ),
    "disabledm": BooleanField("DISABLEDM", True),
    "ifilter": BooleanField("IFILTER", True),
    # Boot animation
    # 480P would be an invalid property name in the namedtuple
    "boot480p": BooleanField("480P", False),
    "cameraview": DiscreteField(
        "CAMERAVIEW", "-1", tuple(str(x) for x in range(-1, 16))
    ),
    "fastani": BooleanField("FASTANI", False),
    "scenecolor1": HexColourField("SCENECOLOR1", "0xFF35FF1A", True),
    "scenecolor2": HexColourField("SCENECOLOR2", "0xFF35FF1A", True),
    "scenecolor3": HexColourField("SCENECOLOR3", "0xFF35FF1A", True),
    "showflub": BooleanField("SHOWFLUB", True),
    "nosound": BooleanField("NOSOUND", False),
    # Blob
    "blobcolor": HexColourField("BLOBCOLOR", "0x40FF27", False),
    "blobradi": IntegerField("BLOBRADI", 23, 0, 100),
    "blobsdead": BooleanField("BLOBSDEAD", False),
    "blobthrob": BooleanField("BLOBTHROB", True),
    "blobbgc": HexColourField("BLOBBGC", "0x000000", False),
    "slowmoblob": BooleanField("SLOWMOBLOB", False),
    "spikeyblob": BooleanField("SPIKEYBLOB", False),
    "customblob": OptionalHDDFilePathField("CUSTOMBLOB", "C:\\flubber.x", "x"),
    "wireframeblob": BooleanField("WIREFRAMEBLOB", False),
    # Fog
    "fogon": BooleanField("FOGON", True),
    # Double check this section
    "fog1abs": BooleanField("FOG1ABS", False),
    "fog1color": HexColourField("FOG1COLOR", "0xFF35FF1A", True),
    "fog1custom": BooleanField("FOG1CUSTOM", False),
    "fog2color": HexColourField("FOG2COLOR", "0xFF35FF1A", True),
    "fog2custom": BooleanField("FOG2CUSTOM", False),
    # Boot animation glow
    "glowcolor": HexColourField("GLOWCOLOR", "0xA0FF60", False),
    "ioglowcolor": HexColourField("IOGLOWCOLOR", "0xA0FF60", False),
    "noflubbg": BooleanField("NOFLUBBG", False),
    # X screen
    "showxen": BooleanField("SHOWXEN", True),
    "bgcolor": HexColourField("BGCOLOR", "0xFFFFFF", False),
    "skewen": BooleanField("SKEWEN", True),
    "tms": BooleanField("TMS", True),
    # The X on the X screen
    "ind3d": BooleanField("IND3D", True),
    "lipcolor": HexColourField("LIPCOLOR", "0x000100", False),
    "lipglow": HexColourField("LIPGLOW", "0x4b9b4b", False),
    "xboxcolor": HexColourField("XBOXCOLOR", "0x62ca13", False),
    "xglowcolor": HexColourField("XGLOWCOLOR", "0xCADE00", False),
    "xinnercolor": HexColourField("XINNERCOLOR", "0x206a16", False),
    "xlightcolor": HexColourField("XLIGHTCOLOR", "0xff000000", True),
    "yskewlogo": IntegerField("YSKEWLOGO", -20, -100, 100),
    "xskewlogo": IntegerField("XSKEWLOGO", 0, -100, 100),
    "xscewxlogo": IntegerField("XSKEWXLOGO", 0, -100, 100),
    "yskewxlogo": IntegerField("YSKEWXLOGO", 0, -100, 100),
    "xlogoscale": IntegerField("XLOGOSCALE", 100, 0, 100),
    "customx": OptionalHDDFilePathField("CUSTOMX", "C:\\xlogo.x", "x"),
    # MS logo
    "showmsen": BooleanField("SHOWMSEN", True),
    "mslogotransen": BooleanField("MSLOGOTRANSEN", False),
    "mslogotranscolor": HexColourField("MSLOGOTRANSCOLOR", "0xff00ff", False),
    "nolighten": BooleanField("NOLIGHTEN", False),
    "customlogo": OptionalHDDFilePathField("CUSTOMLOGO", "C:\\mslogo.bmp", "bmp"),
    # Xbox text
    "xskewtext": IntegerField("XSKEWTEXT", 0, -100, 100),
    "yskewtext": IntegerField("YSKEWTEXT", 0, -100, 100),
    "textscale": IntegerField("TEXTSCALE", 100, 0, 100),
    "customtext": OptionalHDDFilePathField("CUSTOMTEXT", "C:\\text.x", "x"),
    "intro": BooleanField("INTRO", True),
    # Boot order
    "dash1": HDDFilePathField("DASH1", "C:\\evoxdash.xbe", "xbe"),
    "dash2": HDDFilePathField("DASH2", "C:\\nexgen.xbe", "xbe"),
    "dash3": HDDFilePathField("DASH3", "C:\\avalaunch.xbe", "xbe"),
    "defaultxbe": DVDFilePathField("DEFAULTXBE", "D:\\default.xbe", "xbe"),
    "usexbx": BooleanField("USEXBX", False),
}

# Better to use a named tuple as this is accessible globally and named tuples are immutable
IND_BIOS_FIELDS = namedtuple("GenericDict", _IND_BIOS_FIELDS.keys())(**_IND_BIOS_FIELDS)
