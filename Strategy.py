
import OrderTypes
import common
import Stockpyler
import utils
from collections import defaultdict

class Strategy(utils.NextableClass):

    def __init__(self, stockpyler: Stockpyler.Stockpyler, *args, **kwargs):
        super().__init__()
        self._sp = stockpyler
        self._indicators = defaultdict(lambda: [])
        self._pending_orders = []

    def add_indicator(self, security, ind):
        self._indicators[security].append(ind)

    def stop(self):
        #TODO: liquidate positions
        pass

    def next(self):
        pass
        #for ind in self._indicators[s]:
        #    for s in self.get_trading_securities():
        #        ind.next()

    def get_position(self, security):
        return self._sp.pm.position_size(security)

    def get_value(self):
        return self._sp.pm.get_current_value()

    def get_trading_securities(self):
        yield from self._sp.hm.get_trading_securities()

    def get_num_trading_securities(self):
        return self._sp.hm.get_num_trading_securities()

    def today(self):
        return self._sp.hm.today

    def is_trading(self, security):
        #TODO: fix
        return False

    #TODO: move actual impls to Stockpyler class?
    def buy(self, security, quantity):
        o = OrderTypes.MarketOrder(security, common.OrderAction.BUY, quantity)
        o = self._sp.pm.simple_order(o)
        self._pending_orders.append(o)
        return o

    def sell(self, security, quantity):
        o = OrderTypes.MarketOrder(security, common.OrderAction.SELL, quantity)
        o = self._sp.pm.simple_order(o)
        self._pending_orders.append(o)
        return o

    def close(self, security, quantity):
        current_posititon = self._sp.pm.position_size(security)
        assert current_posititon != 0, "You can't close out an empty position!"
        act = common.OrderAction.SELL if current_posititon > 0 else common.OrderAction.BUY

        o = OrderTypes.MarketOrder(security, act, quantity)
        o = self._sp.pm.simple_order(o)
        self._pending_orders.append(o)
        return o

