
import OrderTypes
import Stockpyler
import common


class Strategy:

    def __init__(self, stockpyler: Stockpyler.Stockpyler, *args, **kwargs):
        self._sp = stockpyler
        self._pending_orders = []

    def ohlvc(self, security, index):
        return self._sp.hm.ohlcv(security,index)

    def stop(self):
        #TODO: liquidate positions
        pass

    def next(self):
        pass

    def get_position(self, security):
        return self._sp.pm.position_size(security)

    def get_value(self):
        return self._sp.pm.get_current_value()

    def get_cash(self):
        return self._sp.pm.get_current_cash()

    def get_trading_securities(self):
        return self._sp.hm.get_trading_securities()

    def get_num_trading_securities(self):
        return self._sp.hm.get_num_trading_securities()

    def today(self):
        return self._sp.hm.today

    def is_trading(self, security):
        #TODO: fix
        return False

    def buy(self, security, quantity):
        return self._sp.pm.buy(security, quantity)

    def sell(self, security, quantity):
        return self._sp.pm.sell(security, quantity)

    def close(self, security, quantity):
        return self._sp.pm.close(security, quantity)

