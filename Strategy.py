import abc
import talib
import OrderTypes
import common

import Stockpyler

class Strategy:

    def __init__(self, stockpyler: Stockpyler.Stockpyler, securities, histories, *args, **kwargs):
        self._done = False
        self._sp = stockpyler
        self._securities = securities
        self._histories = histories

    def _next(self):
        done = True
        for s, h in self._histories.items():
            h.next()
            h._next()
            if not h._done:
                done = False
        self._done = done
        #pass

    def _stop(self):
        pass

    @abc.abstractmethod
    def next(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    def get_position(self, security):
        return 0

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

