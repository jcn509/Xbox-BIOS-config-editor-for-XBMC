from StringIO import StringIO

from .abstract_config import AbstractConfig


class AbstractSectionlessConfig(AbstractConfig):
    """
    Extends ConfigParser to allow files without sections.

    This is done by wrapping read files and prepending them with a placeholder
    section.
    """

    def __init__(self, *args, **kwargs):
        default_section = kwargs.pop('default_section', None)
        super(AbstractSectionlessConfig, self).__init__(*args, **kwargs)

    def set(self, section, option, value):
        default_section = self.get_default_section()
        if section != default_section:
            raise ValueError(section + " must be " + default_section)
        super(AbstractSectionlessConfig, self).set(section, option, value)

    def readfp(self, fp, set_invalid_fields_to_default=True, *args, **kwargs):
        stream = StringIO()

        try:
            stream.name = fp.name
        except AttributeError:
            pass

        stream.write('[' + self.get_default_section() + ']\n')
        stream.write(fp.read())
        stream.seek(0, 0)

        ret = super(AbstractSectionlessConfig, self).readfp(stream,
                                                            set_invalid_fields_to_default=set_invalid_fields_to_default,
                                                            *args, **kwargs)
        return ret

    def write(self, fp, dont_write_if_default=True):
        stream = StringIO()
        super(AbstractSectionlessConfig, self).write(stream, dont_write_if_default=dont_write_if_default)
        # Ignore the first line which will be the marker for the default section
        stream.seek(0, 0)
        stream.readline()
        fp.write(stream.read())
