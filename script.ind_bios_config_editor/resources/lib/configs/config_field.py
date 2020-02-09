class ConfigField(object):
    __slots__ = "_default_value", "_field_name", "_validator", "_format_converter"

    def __init__(self, field_name, default_value, validator, format_converter):
        self._default_value = default_value
        self._field_name = field_name
        self._validator = validator
        self._format_converter = format_converter

    # default_value should be read only
    @property
    def default_value(self):
        return self._default_value

    # field_name should be read only
    @property
    def field_name(self):
        return self._field_name

    # validator should be read only
    @property
    def validator(self):
        return self._validator

    # format_converter should be read only
    @property
    def format_converter(self):
        return self._format_converter
