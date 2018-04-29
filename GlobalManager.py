import DataManager
import HistoryManager
import OrderManager
import PositionManager
import TimeManager


class GlobalManager:

    def __init__(self, live, interval, interval_type):

        self.live = live

        self.dm = DataManager.DataManager(self)
        self.hm = HistoryManager.HistoryManager(self)
        self.om = OrderManager.OrderManager(self)
        self.pm = PositionManager.PositionManager(self)
        self.tm = TimeManager.TimeManager(self)

        self.interval = interval
        self.interval_type = interval_type

    def doing_backtest(self):
        return self.live
