
class ConfigError(Exception):
    pass

class ConfigFieldNameError(ConfigError):
    pass

class ConfigFieldValueError(ConfigError):
    pass

class ConfigPresetDoesNotExistError(ConfigError):
    pass
