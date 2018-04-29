
import common
import OrderTypes
import OrderManager



class PositionManager():
    def __init__(self, global_manager, initial_capital=1000000.0, stock_margin = .5, future_margin = .1):
        self.gm = global_manager
        self.capital = initial_capital
        self.stock_margin = stock_margin
        self.future_margin = future_margin
        self.margin = 0.
        self.securities = dict()

    def add_position(self, symbol, num_contracts):
        if symbol not in self.securities:
            self.securities[symbol] = 0

        self.securities[symbol] += num_contracts

        if self.securities[symbol] == 0:
            del self.securities[symbol]

    def position_size(self, symbol):
        if symbol in self.securities:
            return self.securities[symbol]
        raise KeyError("No position in {}".format(symbol))

    def positions(self):
        return self.securities.keys()

    def in_position(self, symbol):
        return self.position_size(symbol) != 0

    def liquidate(self, symbol):
        size = self.position_size(symbol)
        action = 'BUY' if size < 0 else 'SELL'
        o = OrderTypes.MarketOrder(symbol, action, size)
        self.gm.om.simple(o)

    def liquidate_all(self):
        for symbol in self.positions():
            self.liquidate(symbol)

    def can_place_order(self, order):
        # we can always liquidate a position
        if self.in_position(order.security.symbol):
            if self.position_size(order.security.symbol) > 0 and order.action == 'SELL':
                return True
            if self.position_size(order.security.symbol) < 0 and order.action == 'BUY':
                return True

        # Let's always leave a little wiggle room
        return self.calculate_margin_impact(order) > self.capital + 1000

    def execute_order(self, order):
        assert(self.can_place_order(order), "Placed an order when unable to do so!")

        ohlc = self.gm.dm.get_latest(order.security, self.gm.interval, self.gm.interval_type)
        executed, price = order.test(ohlc)

        if liquidating_position(order.action, self.position_size(order.security.symbol)):
            self.capital += total_price
        else:
            self.capital -= total_price

        self.add_position(order.security.symbol, order.num_contracts)

    def calculate_net_position(self, order):


    def calculate_margin_impact(self, order):
        ohlc = self.gm.dm.get_latest(order.security, self.gm.interval, self.gm.interval_type)
        executed, price = order.test(ohlc)
        assert(executed, "Only support market orders right now!")
        total_price = abs(order.num_contracts * price)
        margin_percent = self.future_margin if order.security.security_type == common.SecurityType.FUTURE else self.stock_margin
        return margin_percent * total_price
