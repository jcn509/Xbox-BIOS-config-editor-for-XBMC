from .abstract_sectionless_config import AbstractSectionlessConfig
from .format_converters import *
from .config_validators import *
from .config_field import ConfigField
from .types.ind_bios import Fields


class IndBiosConfig(AbstractSectionlessConfig):
    def __init__(self, *args, **kwargs):
        super(IndBiosConfig, self).__init__(*args, max_line_length=300, quote_char_if_whitespace='"', **kwargs)

    def _get_fields(self):
        return {self.get_default_section(): (
            ConfigField(Fields.AUTOLOADDVD, 1, BooleanField(), Integer()),
            ConfigField(Fields.AVCHECK, 1, BooleanField(), Integer()),
            ConfigField(Fields.IGRLOADSDASH, 0, BooleanField(), Integer()),
            ConfigField(Fields.IGRMODE, 2, DiscreteField([0, 1, 2])),
            ConfigField(Fields.RESETONEJECT, 0, BooleanField(), Integer()),
            ConfigField(Fields.FANSPEED, 10, DiscreteField(xrange(10, 51)), Integer()),
            ConfigField(Fields.LEDPATTERN, "GGGG", RegexMatchPatternField("^[GROBN]{4}$"), None),
            ConfigField(Fields.NOSOUND, 0, BooleanField(), Integer()),
            ConfigField(Fields.BOOTANIMATION480P, 0, BooleanField(), Integer()),
            ConfigField(Fields.BLOBCOLOR, "0x40FF27", ColourField(), None),
            ConfigField(Fields.BLOBRADI, 23, ZeroToAHundredField(), Integer()),
            ConfigField(Fields.BLOBSDEAD, 0, BooleanField(), Integer()),
            ConfigField(Fields.BLOBTHROB, 1, BooleanField(), Integer()),
            ConfigField(Fields.CAMERAVIEW, -1, DiscreteField(xrange(-1, 16))),
            ConfigField(Fields.FASTANI, 0, BooleanField(), Integer()),
            ConfigField(Fields.BLOBBGC, "0x000000", ColourField(), None),
            ConfigField(Fields.FOGON, 1, BooleanField(), Integer()),
            # Double check this section
            ConfigField(Fields.FOG1ABS, 0, BooleanField(), Integer()),
            ConfigField(Fields.FOG1COLOR, "0xFF35FF1A", ColourWithAlphaField(), None),
            ConfigField(Fields.FOG1CUSTOM, 0, BooleanField(), Integer()),
            ConfigField(Fields.FOG2COLOR, "0xFF35FF1A", ColourWithAlphaField(), None),
            ConfigField(Fields.FOG2CUSTOM, 0, BooleanField(), Integer()),
    
            ConfigField(Fields.GLOWCOLOR, "0xA0FF60", ColourField(), None),
            ConfigField(Fields.IOGLOWCOLOR, "0xA0FF60", ColourField(), None),
            ConfigField(Fields.NOFLUBBG, 0, BooleanField(), Integer()),
    
            ConfigField(Fields.SCENECOLOR1, "0xFF35FF1A", ColourWithAlphaField(), None),
            ConfigField(Fields.SCENECOLOR2, "0xFF35FF1A", ColourWithAlphaField(), None),
            ConfigField(Fields.SCENECOLOR3, "0xFF35FF1A", ColourWithAlphaField(), None),
    
            ConfigField(Fields.SHOWFLUB, 1, BooleanField(), Integer()),
            ConfigField(Fields.IFILTER, 1, BooleanField(), Integer()),
            ConfigField(Fields.SLOWMOBLOB, 0, BooleanField(), Integer()),
            ConfigField(Fields.SPIKEYBLOB, 0, BooleanField(), Integer()),
            ConfigField(Fields.CUSTOMBLOB, "\\Device\\Harddisk0\\Partition2\\flubber.x", ModelFileField()),
            ConfigField(Fields.WIREFRAMEBLOB, 0, BooleanField(), Integer()),
            ConfigField(Fields.SHOWMSEN, 1, BooleanField(), Integer()),
            ConfigField(Fields.SHOWXEN, 1, BooleanField(), Integer()),
            ConfigField(Fields.BGCOLOR, "0xFFFFFF", ColourField(), None),
            ConfigField(Fields.IND3D, 1, BooleanField(), Integer()),
            ConfigField(Fields.LIPCOLOR, "0x000100", ColourField(), None),
            ConfigField(Fields.LIPGLOW, "0x4b9b4b", ColourField(), None),
            ConfigField(Fields.MSLOGOTRANSEN, 0, BooleanField(), Integer()),
            ConfigField(Fields.MSLOGOTRANSCOLOR, 0, BooleanField(), Integer()),
            ConfigField(Fields.NOLIGHTEN, 0, BooleanField(), Integer()),
            ConfigField(Fields.TMS, 1, BooleanField(), Integer()),
            ConfigField(Fields.XBOXCOLOR, "0x62ca13", ColourField(), None),
            ConfigField(Fields.XGLOWCOLOR, "0xCADE00", ColourField(), None),
            ConfigField(Fields.XINNERCOLOR, "0x206a16", ColourField(), None),
            ConfigField(Fields.XLIGHTCOLOR, "0xff000000", ColourWithAlphaField(), None),
    
            ConfigField(Fields.SKEWEN, 1, BooleanField(), Integer()),
            ConfigField(Fields.YSKEWLOGO, -20, PositionField(), Integer()),
            ConfigField(Fields.XSKEWLOGO, 0, PositionField(), Integer()),
    
            ConfigField(Fields.XSKEWXLOGO, 0, PositionField(), Integer()),
            ConfigField(Fields.YSKEWXLOGO, 0, PositionField(), Integer()),
            ConfigField(Fields.XLOGOSCALE, 100, ZeroToAHundredField(), Integer()),
    
            ConfigField(Fields.XSKEWTEXT, 0, PositionField(), Integer()),
            ConfigField(Fields.YSKEWTEXT, 0, PositionField(), Integer()),
            ConfigField(Fields.TEXTSCALE, 100, ZeroToAHundredField(), Integer()),
            ConfigField(Fields.CUSTOMLOGO, "\\Device\\Harddisk0\\Partition2\\mslogo.bmp", HddFilePathOrZeroField("bmp"),
                        DosFilePathOrZero()),
            ConfigField(Fields.CUSTOMX, "\\Device\\Harddisk0\\Partition2\\xlogo.x", ModelFileField(),
                        DosFilePathOrZero()),
            ConfigField(Fields.CUSTOMTEXT, "\\Device\\Harddisk0\\Partition2\\text.x", ModelFileField(),
                        DosFilePathOrZero()),
            ConfigField(Fields.INTRO, 1, BooleanField(), Integer()),
            ConfigField(Fields.DASH1, "\\Device\\Harddisk0\\Partition2\\evoxdash.xbe", HddXbeFileField(),
                        DosFilePath()),
            ConfigField(Fields.DASH2, "\\Device\\Harddisk0\\Partition2\\nexgen.xbe", HddXbeFileField(), DosFilePath()),
            ConfigField(Fields.DASH3, "\\Device\\Harddisk0\\Partition2\\avalaunch.xbe", HddXbeFileField(),
                        DosFilePath()),
            ConfigField(Fields.DEFAULTXBE, "\\Device\\CdRom0\\default.xbe", DvdXbeFileField(), DosFilePath()),
            ConfigField(Fields.USEXBX, 0, BooleanField(), Integer()),
            ConfigField(Fields.USEALLMEMORY, 0, BooleanField(), Integer()),
            ConfigField(Fields.MACADDR, "00:00:00:00:00:00",
                        RegexMatchPatternField("^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$"), None),
            ConfigField(Fields.DISABLEDM, 1, BooleanField(), Integer())
        )}

    def _get_true_if_non_default(self):
        return {self.get_default_section(): {
            "FOG1CUSTOM": ["FOG1COLOR"],
            "FOG2CUSTOM": ["FOG2COLOR"]
        }}

    def _get_true_if_non_zero(self):
        return {self.get_default_section(): {
            "SKEWEN": ["XSKEWLOGO", "YSKEWLOGO"]
        }}
