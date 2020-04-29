from abc import ABCMeta, abstractmethod


class AbstractFormatConverter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def convert_to_config_file_format(self, value):
        raise NotImplementedError

    @abstractmethod
    def convert_to_xbmc_control_format(self, value):
        raise NotImplementedError
