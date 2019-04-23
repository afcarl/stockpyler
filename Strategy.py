import abc
import talib
import OrderTypes
import common
import itertools
import Stockpyler
import utils
from collections import defaultdict

class Strategy(utils.NextableClass):

    def __init__(self, stockpyler: Stockpyler.Stockpyler, securities, histories, *args, **kwargs):
        super().__init__()
        self._sp = stockpyler
        self._securities = securities
        self._histories = histories
        self._indicators = defaultdict(lambda: [])
        self.add_nextable(*histories.values())

    def add_indicator(self, security, ind):
        self._indicators[security].append(ind)

    def stop(self):
        #TODO: liquidate positions
        pass

    def next(self):
        for s in self.get_trading_securities():
            for ind in self._indicators[s]:
                ind.next()

    def get_position(self, security):
        return self._sp.pm.position_size(security)

    def get_value(self):
        return self._sp.pm.get_current_value()

    def get_trading_securities(self):
        yield from self._sp.hm.get_trading_securities()

    def today(self):
        return self._sp.hm.today

    def is_trading(self, security):
        today = self.today()
        history = self._histories[security]
        return today == history.datetime[0]

    #TODO: move actual impls to Stockpyler class?
    def buy(self, security, quantity):
        o = OrderTypes.MarketOrder(security, common.OrderAction.BUY, quantity)
        o = self._sp.pm.simple_order(o)
        return o

    def sell(self, security, quantity):
        o = OrderTypes.MarketOrder(security, common.OrderAction.SELL, quantity)
        o = self._sp.pm.simple_order(o)
        return o

    def close(self, security, quantity):
        current_posititon = self._sp.pm.position_size(security)
        assert current_posititon != 0, "You can't close out an empty position!"
        act = common.OrderAction.SELL if current_posititon > 0 else common.OrderAction.BUY

        o = OrderTypes.MarketOrder(security, act, quantity)
        o = self._sp.pm.simple_order(o)
        return o

