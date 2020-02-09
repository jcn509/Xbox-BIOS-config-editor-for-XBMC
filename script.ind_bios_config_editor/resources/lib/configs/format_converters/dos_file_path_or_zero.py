from .dos_file_path import DosFilePath


class DosFilePathOrZero(DosFilePath):

    def convert_to_config_file_format(self, value):
        if value != '0':
            value = super(DosFilePathOrZero).convert_to_config_file_format(value)
        return value

    def convert_to_xbmc_control_format(self, value):
        if value != '0':
            value = super(DosFilePathOrZero).convert_to_xbmc_control_format(value)
        return value
