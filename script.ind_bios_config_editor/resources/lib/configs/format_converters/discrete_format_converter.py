from .abstract_format_converter import AbstractFormatConverter


class DiscreteFormatConverter(AbstractFormatConverter):
    def __init__(self, values):
        self._values = tuple(values)

    def convert_to_config_file_format(self, value):
        return str(self._values.index(value))

    def convert_to_python_format(self, value):
        return self._values[int(value)]
