from .dos_file_path_format_converter import DosFilePathFormatConverter


class DosFilePathOrZeroFormatConverter(DosFilePathFormatConverter):

    def convert_to_config_file_format(self, value):
        if value != '0':
            value = super(DosFilePathOrZeroFormatConverter, self).convert_to_config_file_format(value)
        return value

    def convert_to_xbmc_control_format(self, value):
        if value != '0':
            value = super(DosFilePathOrZeroFormatConverter, self).convert_to_xbmc_control_format(value)
        return value
