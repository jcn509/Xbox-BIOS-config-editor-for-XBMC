"""Exceptions that may thrown by AbstractConfig"""


class ConfigError(Exception):
    """Generic config error (useful to catch all config errors)"""

    pass


class ConfigFieldNameError(ConfigError):
    """Config field name is not correct"""

    pass


class ConfigFieldValueError(ConfigError):
    """Config field value is not correct"""

    pass


class ConfigPresetDoesNotExistError(ConfigError):
    """The chosen preset does not exist"""

    pass
