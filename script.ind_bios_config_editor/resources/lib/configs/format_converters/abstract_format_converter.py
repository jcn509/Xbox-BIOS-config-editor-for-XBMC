"""Abstract format converter. Format converters convert values between their
"Python" format and "config file" format
"""

from abc import ABCMeta, abstractmethod

try:
    # typing not available on XBMC4XBOX
    from typing import Any
except:
    pass

class AbstractFormatConverter(object):
    """Used to convert values between their "config file" and "Python" formats
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert_to_config_file_format(self, value):
        """Convert the given value from its Python format to its config file
        format
        """
        # type: (Any) -> str
        raise NotImplementedError

    @abstractmethod
    def convert_to_python_format(self, value):
        """Convert the given value from its config file format to its Python
        format
        """
        # type: (str) -> Any
        raise NotImplementedError
