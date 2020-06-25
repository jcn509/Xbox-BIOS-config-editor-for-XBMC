"""Abstract class to ensure that all controls with state have the same
interface
"""
from abc import ABCMeta, abstractmethod

try:
    # typing not available on XBMC4Xbox
    from typing import Any
except:
    pass


class AbstractControl(object):
    """Implemented by all controls with state to ensure that they have the
    same interface
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_value(self, value, trigger_callback=True):
        """:param trigger_callback: trigger callback connected to this control
        """
        # type: (Any, bool) -> None
        pass

    @abstractmethod
    def get_value(self):
        # type: () -> Any
        pass
