import matplotlib.pyplot as plt

import HistoryManager
import PositionManager


class Stockpyler:

    def __init__(self, live=False):
        self.live = live

        self.hm = HistoryManager.HistoryManager(self)
        self.pm = PositionManager.PositionManager(self)

        #3ple of strategy class, args, kwargs
        self.strategies = []
        self.observers = []
        self.running_strategies = []
        self.running_observers = []

    def doing_backtest(self):
        return self.live

    def add_strategy(self, strategy, *args, **kwargs):
        self.strategies.append((strategy, args, kwargs))

    def add_observer(self, observer, *args, **kwargs):
        self.observers.append((observer, args, kwargs))

    def init_strategies(self):
        for s, args, kwargs in self.strategies:
            strat_obj = s(self, *args, **kwargs)
            self.running_strategies.append(strat_obj)

    def init_observers(self):
        for s, args, kwargs in self.observers:
            observer_obj = s(self, *args, **kwargs)
            self.running_observers.append(observer_obj)

    def init(self):
        self.init_strategies()
        self.init_observers()
        self.hm.start()

    def run(self):
        self.init()
        counter = 0
        while not self.hm._done:
            for s in self.running_strategies:
                s.next()
            for o in self.running_observers:
                o.next()
            self.pm.next()
            self.hm.next()
        for s in self.running_strategies:
            s.stop()

    def show(self):
        plt.title("My backtest")
        obs = self.running_observers[0]
        x = list(obs._dt_value_map.keys())
        y = list(obs._dt_value_map.values())
        plt.plot(x,y)
        plt.show()


