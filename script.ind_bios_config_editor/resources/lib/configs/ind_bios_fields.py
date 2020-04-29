from .config_field import BooleanField, IntegerField, DiscreteField, StringField, HDDFilePathField, OptionalHDDFilePathField, DVDFilePathField, HexColourField

IND_BIOS_FIELDS = (
    BooleanField("AUTOLOADDVD", True),
    BooleanField("AVCHECK", True),
    BooleanField("IGRLOADSDASH", False),
    DiscreteField("IGRMODE", "Quick", ("Off", "Compatible", "Quick")),
    BooleanField("RESETONEJECT", False),
    IntegerField("FANSPEED", 10, 10, 50),
    StringField("LEDPATTERN", "GGGG", r"^[GROBN]{4}$"),
    BooleanField("USEALLMEMORY", False),
    StringField("MACADDR", "00:00:00:00:00:00", r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"),
    BooleanField("DISABLEDM", True),
    BooleanField("IFILTER", True),

    # Boot animation
    BooleanField("480P", False),
    IntegerField("CAMERAVIEW", -1, -1, 15),
    BooleanField("FASTANI", False),
    HexColourField("SCENECOLOR1", "0xFF35FF1A", True),
    HexColourField("SCENECOLOR2", "0xFF35FF1A", True),
    HexColourField("SCENECOLOR3", "0xFF35FF1A", True),
    BooleanField("SHOWFLUB", True),
    BooleanField("NOSOUND", False),

    # Blob
    HexColourField("BLOBCOLOR", "0x40FF27", False),
    IntegerField("BLOBRADI", 23, 0, 100),
    BooleanField("BLOBSDEAD", False),
    BooleanField("BLOBTHROB", True),
    HexColourField("BLOBBGC", "0x000000", False),
    BooleanField("SLOWMOBLOB", False),
    BooleanField("SPIKEYBLOB", False),
    OptionalHDDFilePathField("CUSTOMBLOB", "C:\\flubber.x", "x"),
    BooleanField("WIREFRAMEBLOB", False),

    # Fog
    BooleanField("FOGON", True),
    # Double check this section
    BooleanField("FOG1ABS", False),
    HexColourField("FOG1COLOR", "0xFF35FF1A", True),
    BooleanField("FOG1CUSTOM", False),
    HexColourField("FOG2COLOR", "0xFF35FF1A", True),
    BooleanField("FOG2CUSTOM", False),

    # Boot animation glow
    HexColourField("GLOWCOLOR", "0xA0FF60", False),
    HexColourField("IOGLOWCOLOR", "0xA0FF60", False),
    BooleanField("NOFLUBBG", False),
    
    # X screen
    BooleanField("SHOWXEN", True),
    HexColourField("BGCOLOR", "0xFFFFFF", False),
    BooleanField("SKEWEN", True),
    BooleanField("TMS", True),
    
    # X
    BooleanField("IND3D", True),
    HexColourField("LIPCOLOR", "0x000100", False),
    HexColourField("LIPGLOW", "0x4b9b4b", False),
    HexColourField("XBOXCOLOR", "0x62ca13", False),
    HexColourField("XGLOWCOLOR", "0xCADE00", False),
    HexColourField("XINNERCOLOR", "0x206a16", False),
    HexColourField("XLIGHTCOLOR", "0xff000000", True),
    IntegerField("YSKEWLOGO", -20, -100, 100),
    IntegerField("XSKEWLOGO", 0, -100, 100),
    IntegerField("XSKEWXLOGO", 0, -100, 100),
    IntegerField("YSKEWXLOGO", 0, -100, 100),
    IntegerField("XLOGOSCALE", 100, 0, 100),
    OptionalHDDFilePathField("CUSTOMX", "C:\\xlogo.x", "x"),

    # MS logo
    BooleanField("SHOWMSEN", True),
    BooleanField("MSLOGOTRANSEN", False),
    BooleanField("MSLOGOTRANSCOLOR", False),
    BooleanField("NOLIGHTEN", False),
    OptionalHDDFilePathField("CUSTOMLOGO", "C:\\mslogo.bmp", "bmp"),
    
    # Xbox text
    IntegerField("XSKEWTEXT", 0, -100, 100),
    IntegerField("YSKEWTEXT", 0, -100, 100),
    IntegerField("TEXTSCALE", 100, 0, 100),
    OptionalHDDFilePathField("CUSTOMTEXT", "C:\\text.x", "x"),
    BooleanField("INTRO", True),

    # Boot order
    HDDFilePathField("DASH1", "C:\\evoxdash.xbe", "xbe"),
    HDDFilePathField("DASH2", "C:\\nexgen.xbe", "xbe"),
    HDDFilePathField("DASH3", "C:\\avalaunch.xbe", "xbe"),
    DVDFilePathField("DEFAULTXBE", "D:\\default.xbe", "xbe"),
    BooleanField("USEXBX", False)
)