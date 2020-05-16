from abc import ABCMeta, abstractmethod
from ..config_errors import ConfigFieldValueError


def raise_error(message):
    raise ConfigFieldValueError(message)


class AbstractValidator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def validate_in_config_format(self, value):
        raise NotImplementedError

    @abstractmethod
    def validate_in_python_format(self, value):
        raise NotImplementedError
