from abc import ABCMeta, abstractmethod


class AbstractControl(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_value(self, value, trigger_callback=True):
        pass

    @abstractmethod
    def get_value(self, value):
        pass
