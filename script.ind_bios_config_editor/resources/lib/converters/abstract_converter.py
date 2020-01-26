from abc import ABCMeta, abstractmethod

class AbstractConverter(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._control_to_config = {}
        self._config_to_control = {}
    
    def register_config_to_control_converter(self, section, field, converter):
        if section not in self._config_to_control:
            self._config_to_control[section] = {}
        self._config_to_control[section][field] = converter

    def register_control_to_config_converter(self, section, field, converter):
        if section not in self._control_to_config:
            self._control_to_config[section] = {}
        self._control_to_config[section][field] = converter

    def _convert_boolean_to_control_format(self, value):
        return int(value)

    def _convert_boolean_to_config_format(self, value):
        return str(value)
        
    @abstractmethod
    def convert_to_config_format(self, section, field, value, control):
        pass

    @abstractmethod
    def convert_to_control_format(self, section, field, value, control):
        pass
