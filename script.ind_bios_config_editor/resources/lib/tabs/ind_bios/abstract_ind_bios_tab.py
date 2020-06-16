from ..abstract_tab import AbstractTab


class AbstractIndBiosTab(AbstractTab):
    def __new__(cls, config, num_columns=0, default_columnspan=1):
        # Group.__new__ is not responsible for setting number of rows/columns
        return super(AbstractIndBiosTab, cls).__new__(
            cls, config, num_columns=num_columns, default_columnspan=default_columnspan
        )

    def __init__(self, config, num_columns, default_columnspan=1):

        super(AbstractIndBiosTab, self).__init__(
            config, num_columns=num_columns, default_columnspan=default_columnspan
        )

