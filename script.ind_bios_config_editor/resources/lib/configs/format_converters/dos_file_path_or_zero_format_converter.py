from .dos_file_path_format_converter import DosFilePathFormatConverter


class DosFilePathOrZeroFormatConverter(DosFilePathFormatConverter):

    def convert_to_config_file_format(self, value):
        if value == None:
            return '0'
        return super(DosFilePathOrZeroFormatConverter, self).convert_to_config_file_format(value)

    def convert_to_xbmc_control_format(self, value):
        if value == '0':
            return None
        return super(DosFilePathOrZeroFormatConverter, self).convert_to_xbmc_control_format(value)
