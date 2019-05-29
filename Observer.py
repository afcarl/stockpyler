import math

import Stockpyler

class Observer:

    def __init__(self, stockpyler: Stockpyler.Stockpyler):
        self._sp = stockpyler
        self._dt_value_map = dict()

    def next(self):
        pass

    def today(self):
        return self._sp.hm.today

    def add_value(self, dt, value):
        if self._sp.hm.get_num_trading_securities() == 0:
            return
        if dt not in self._dt_value_map:
            self._dt_value_map[dt] = [value]
        else:
            self._dt_value_map[dt].append(value)


class AccountValueObserver(Observer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        pass

    def next(self):
        dt = self.today()
        v = self._sp.pm.get_current_value()
        self.add_value(dt, math.log(v))
