from common import *

class DataManager:
    __all_managers = []

    def __init__(self, symbol, security_type, interval, interval_type, period, extended=True, adjusted=True):
        self.symbol = symbol
        self.security_type = security_type
        self.interval = interval
        self.interval_type = interval_type
        self.extended = extended
        self.adjusted = adjusted

        if DoingBackTest():
            from kibot import KibotApi
            self.history = KibotApi().request(symbol, security_type, interval, interval_type, period, adjusted, extended)
            self.position = 0

        DataManager.__all_managers.append(self)

    def get_latest(self, period=1, offset=0):
        assert(offset >= 0, "Can't look into the future!")
        if DoingBackTest():
            begin = self.position - period - offset
            if begin < 0:
                begin = 0

            return self.history[begin:self.position - offset]
        else:
            #do IB stuff
            pass

    def advance_time(self):
        if not DoingBackTest():
            raise ValueError("Cannot advance time during live trading!")
        self.position += 1




