import DataManager
import HistoryManager
import OrderManager
import PositionManager
import TimeManager


class GlobalManager:

    def __init__(self, live=False):

        self.live = live

        self.dm = DataManager.DataManager(self)
        self.hm = HistoryManager.HistoryManager(self)
        self.om = OrderManager.OrderManager(self)
        self.pm = PositionManager.PositionManager(self)
        self.tm = TimeManager.TimeManager(self)


    def doing_backtest(self):
        return self.live
