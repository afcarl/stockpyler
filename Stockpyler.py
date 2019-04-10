import DataManager
import HistoryManager
import PositionManager
import TimeManager


class Stockpyler:

    def __init__(self, live=False):

        self.live = live

        self.dm = DataManager.DataManager(self)
        self.hm = HistoryManager.HistoryManager(self)
        self.pm = PositionManager.PositionManager(self)
        self.tm = TimeManager.TimeManager(self)

    def doing_backtest(self):
        return self.live

    def add_history(self, security, csv):
        return self.hm.add_history(security, csv)
