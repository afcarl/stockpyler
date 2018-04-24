import common
from TimeManager import TimeManager
from HistoryManager import HistoryManager


class DataManager(metaclass=common.Singleton):

    def __init__(self):
        self.tm = TimeManager()
        self.hm = HistoryManager()

    def get_latest(self, security, interval, interval_type, period=1, offset=0):
        assert(offset >= 0, "Can't look into the future!")
        if self.tm.doing_backtest():
            return self.hm.get_history(security, interval, interval_type, period, offset)
        else:
            #do IB stuff
            pass

