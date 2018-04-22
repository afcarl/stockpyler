from common import *
from DataManager import DataManager

class Security:

    def __init__(self, symbol,
                 security_type,
                 interval=1,
                 interval_type='minute',
                 period=1,
                 extended=None,
                 adjusted=None):

        self.symbol = symbol
        self.security_type = security_type
        self.interval = interval
        self.interval_type = interval_type
        self.period = period
        self.extended_hours = extended
        self.adjusted = adjusted

        self.data_manager = DataManager(symbol,security_type,interval,interval_type,period,extended,adjusted)

    def get_latest(self, period):
        return self.data_manager.get_latest(period)


