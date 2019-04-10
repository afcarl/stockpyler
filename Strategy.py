import abc
import talib
import OrderTypes
import common

import Stockpyler

class Strategy:

    def __init__(self, stockpyler: Stockpyler.Stockpyler, securities, histories, *args, **kwargs):
        self._sp = stockpyler
        self._securities = securities
        self._histories = histories

    @abc.abstractmethod
    def next(self):
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

    def done(self):
        if not self.gm.tm.doing_backtest():
            raise ValueError("Can't be done during live trading!")
        return self.done
