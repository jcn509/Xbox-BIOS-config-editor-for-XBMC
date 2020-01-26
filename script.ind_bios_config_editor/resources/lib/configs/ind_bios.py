from .abstract_sectionless_config import AbstractSectionlessConfig
from config_validators import *


class IndBiosConfig(AbstractSectionlessConfig):
    def __init__(self, *args, **kwargs):
        super(IndBiosConfig, self).__init__(*args, max_line_length=300, quote_char_if_whitespace='"', **kwargs)

    def _get_fields(self):
        return {self.get_default_section(): [
            BooleanField("AUTOLOADDVD", 1),
            BooleanField("AVCHECK", 1),
            BooleanField("IGRLOADSDASH", 0),
            DiscreteField("IGRMODE", 2, [0, 1, 2]),
            BooleanField("RESETONEJECT", 0),
            DiscreteField("FANSPEED", 10, xrange(10, 51)),
            RegexMatchPatternField("LEDPATTERN", "GGGG", "^[GROBN]{4}$"),
            BooleanField("NOSOUND", 0),
            BooleanField("480P", 0),
            ColourField("BLOBCOLOR", "0x40FF27"),
            ZeroToAHundredField("BLOBRADI", 23),
            BooleanField("BLOBSDEAD", 0),
            BooleanField("BLOBTHROB", 1),
            DiscreteField("CAMERAVIEW", -1, xrange(-1, 16)),
            BooleanField("FASTANI", 0),
            ColourField("BLOBBGC", "0x000000"),
            BooleanField("FOGON", 1),
            # Double check this section
            BooleanField("FOG1ABS", 0),
            ColourWithAlphaField("FOG1COLOR", "0xFF35FF1A"),
            BooleanField("FOG1CUSTOM", 0),
            ColourWithAlphaField("FOG2COLOR", "0xFF35FF1A"),
            BooleanField("FOG2CUSTOM", 0),

            ColourField("GLOWCOLOR", "0xA0FF60"),
            ColourField("IOGLOWCOLOR", "0xA0FF60"),
            BooleanField("NOFLUBBG", 0),

            ColourWithAlphaField("SCENECOLOR1", "0xFF35FF1A"),
            ColourWithAlphaField("SCENECOLOR2", "0xFF35FF1A"),
            ColourWithAlphaField("SCENECOLOR3", "0xFF35FF1A"),

            BooleanField("SHOWFLUB", 1),
            BooleanField("IFILTER", 1),
            BooleanField("SLOWMOBLOB", 0),
            BooleanField("SPIKEYBLOB", 0),
            ModelFileField("CUSTOMBLOB", "\\Device\\Harddisk0\\Partition2\\flubber.x"),
            BooleanField("WIREFRAMEBLOB", 0),
            BooleanField("SHOWMSEN", 1),
            BooleanField("SHOWXEN", 1),
            ColourField("BGCOLOR", "0xFFFFFF"),
            BooleanField("IND3D", 1),
            ColourField("LIPCOLOR", "0x000100"),
            ColourField("LIPGLOW", "0x4b9b4b"),
            BooleanField("MSLOGOTRANSEN", 0),
            BooleanField("MSLOGOTRANSCOLOR", 0),
            BooleanField("NOLIGHTEN", 0),
            BooleanField("TMS", 1),
            ColourField("XBOXCOLOR", "0x62ca13"),
            ColourField("XGLOWCOLOR", "0xCADE00"),
            ColourField("XINNERCOLOR", "0x206a16"),
            ColourWithAlphaField("XLIGHTCOLOR", "0xff000000"),

            BooleanField("SKEWEN", 1),
            PositionField("YSKEWLOGO", -20),
            PositionField("XSKEWLOGO", 0),

            PositionField("XSKEWXLOGO", 0),
            PositionField("YSKEWXLOGO", 0),
            ZeroToAHundredField("XLOGOSCALE", 100),

            PositionField("XSKEWTEXT", 0),
            PositionField("YSKEWTEXT", 0),
            ZeroToAHundredField("TEXTSCALE", 100),
            HddFilePathOrZeroField("CUSTOMLOGO", "\\Device\\Harddisk0\\Partition2\\mslogo.bmp", "bmp"),
            ModelFileField("CUSTOMX", "\\Device\\Harddisk0\\Partition2\\xlogo.x"),
            ModelFileField("CUSTOMTEXT", "\\Device\\Harddisk0\\Partition2\\text.x"),
            BooleanField("INTRO", 1),
            HddXbeFileField("DASH1", "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe"),
            HddXbeFileField("DASH2", "\\Device\\Harddisk0\\Partition2\\nexgen.xbe"),
            HddXbeFileField("DASH3", "\\Device\\Harddisk0\\Partition2\\avalaunch.xbe"),
            DvdXbeFileField("DEFAULTXBE", "\\Device\\CdRom0\\default.xbe"),
            BooleanField("USEXBX", 0),
            BooleanField("USEALLMEMORY", 0),
            RegexMatchPatternField("MACADDR", "00:00:00:00:00:00", "^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"),
            BooleanField("DISABLEDM", 1)
        ]}

    def _get_true_if_non_default(self):
        return {self.get_default_section(): {
            "FOG1CUSTOM": ["FOG1COLOR"],
            "FOG2CUSTOM": ["FOG2COLOR"]
        }}

    def _get_true_if_non_zero(self):
        return {self.get_default_section(): {
            "SKEWEN": ["XSKEWLOGO", "YSKEWLOGO"]
        }}
