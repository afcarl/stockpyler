import common
import TimeManager
import HistoryManager


class DataManager:

    def __init__(self, global_manager):
        self.gm = global_manager

    def get_latest(self, security, interval, interval_type, period=1, offset=0):
        assert(offset >= 0, "Can't look into the future!")
        if self.gm.doing_backtest():
            return self.gm.hm.get_history(security, interval, interval_type, period, offset)
        else:
            #do IB stuff
            pass
