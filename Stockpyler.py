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

        #3ple of strategy class, args, kwargs
        self.strategies = []
        self.running_strategies = []

    def doing_backtest(self):
        return self.live

    def add_history(self, security, csv):
        return self.hm.add_history(security, csv)

    def add_strategy(self, strategy, *args, **kwargs):
        self.strategies.append((strategy, args, kwargs))

    def init_strategies(self):
        for s, args, kwargs in self.strategies:
            strat_obj = s(self, *args, **kwargs)
            self.running_strategies.append(strat_obj)

    def init(self):
        self.init_strategies()
        self.hm.start()

    def run(self):
        #tracemalloc.start()
        self.init()
        counter = 0
        while not self.hm._done:
            for s in self.running_strategies:
                s.next()
            self.pm.next()
            self.hm.next()
            counter += 1
            #if counter %1000 == 0:
            #    snapshot = tracemalloc.take_snapshot()
            #    utils.display_top(snapshot)
        for s in self.running_strategies:
            s.stop()


