"""Abstract validator class.
Validators are used to validate values in both their Python and config file
formats
"""
from abc import ABCMeta, abstractmethod
try:
    # typing is not available on XBMC4XBOX
    from typing import Any
except:
    pass
from ..config_errors import ConfigFieldValueError


def raise_error(message):
    """Helper function for raising errors when values are not correctly
    formatted
    """
    raise ConfigFieldValueError(message)


class AbstractValidator(object):
    """Validators are used to validate values in both their Python and config
    file formats
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_in_config_file_format(self, value):
        """Throws an error if the value is not in the correct format"""
        # type: (str) -> None
        raise NotImplementedError

    @abstractmethod
    def validate_in_python_format(self, value):
        """Throws an error if the value is not in the correct format"""
        # type: (Any) -> None
        raise NotImplementedError
