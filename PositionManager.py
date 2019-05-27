import math
import OrderTypes
import common


class PositionManager:
    def __init__(self, stockpyler, initial_cash=10000.0, stock_margin = .5):
        self._sp = stockpyler
        self.current_cash = initial_cash
        self.stock_margin = stock_margin
        self.current_margin = 0.
        self.positions = dict()

        self.orders = list()
        self.current_order_id = 0

    def buy(self, security, quantity):
        if quantity == 0:
            return None
        o = OrderTypes.MarketOrder(security, common.OrderAction.BUY, quantity)
        o = self.simple_order(o)
        return o

    def sell(self, security, quantity):
        if quantity == 0:
            return None
        o = OrderTypes.MarketOrder(security, common.OrderAction.SELL, quantity)
        o = self.simple_order(o)
        return o

    def close(self, security, quantity):
        current_posititon = self._sp.pm.position_size(security)
        assert current_posititon != 0, "You can't close out an empty position!"
        act = common.OrderAction.SELL if current_posititon > 0 else common.OrderAction.BUY

        o = OrderTypes.MarketOrder(security, act, quantity)
        o = self.simple_order(o)
        return o


    def simple_order(self, order):
        assert isinstance(order, OrderTypes.MarketOrder), "Only simple market orders are supported"
        order.id = self.next_order_id()
        self.orders.append(order)
        return order

    def one_cancels_other_order(self, order1, order2):
        assert(False, "Currently only simple market orders are supported")
        self.one_cancels_all_order(order1, order2)

    def one_cancels_all_order(self, *orders):
        assert(False, "Currently only simple market orders are supported")
        ids = [self.next_order_id() for _ in orders]

        for id, order in zip(ids, orders):
            if not self.sp.pm.can_place_order(order):
                return common.OrderExecutionStatus.ORDER_NOT_PLACED
            order.id = id
            order.cancels = list(filter(lambda x: x != id, ids))
            self.orders[id] = order

        return common.OrderExecutionStatus.ORDER_PLACED

    def next_order_id(self):
        self.current_order_id += 1
        return self.current_order_id

    def next(self):
        assert self.current_cash > 0
        new_orders = []
        for p, num_stocks in self.positions.items():
            today = self._sp.hm.today
            if self._sp.hm.start_end_dates[p][1] == today:
                self.close(p, num_stocks)

        for order in self.orders:
            ohlc = self._sp.hm.ohlcv(order.security, 0)
            cash = self.current_cash
            execute, price = order.test(ohlc)
            if execute:
                if self.can_place_order(order):
                    self._sp.pm.execute_order(order, ohlc)
                else:
                    order.status = common.OrderExecutionStatus.MARGIN
            else:
                order.update(ohlc)
                new_orders.append(order)
            assert self.current_cash > 0
        self.orders = new_orders

        assert self.current_cash > 0

    def add_position(self, security, num_contracts):
        if security not in self.positions:
            self.positions[security] = 0

        self.positions[security] += num_contracts

        if self.positions[security] == 0:
            del self.positions[security]

    def position_size(self, security):
        if security in self.positions:
            return self.positions[security]
        return 0

    def get_positions(self):
        return self.positions.keys()

    def in_position(self, security):
        return self.position_size(security) != 0

    def liquidate(self, security):
        size = self.position_size(security)
        action = 'BUY' if size < 0 else 'SELL'
        o = OrderTypes.MarketOrder(security, action, size)
        self._sp.om.simple(o)

    def liquidate_all(self):
        for security in self.get_positions():
            self.liquidate(security)

    def get_current_cash(self):
        return self.current_cash

    def get_current_margin(self):
        return self.current_margin

    def get_current_value(self):
        value = self.get_current_cash()
        if math.isnan(value):
            print('asdf')
        for k, v in self.positions.items():
            ohlvc = self._sp.hm.ohlcv(k, 0)
            if math.isnan(self._sp.hm.ohlcv(k, 0).close):
                print('asdf')
            if math.isnan(v):
                print('asdf')
            value += self._sp.hm.ohlcv(k, 0).close * v
        return value

    def increases_exposure(self, order):
        return self.calculate_margin_impact(order) > 0

    def can_place_order(self, order, ohlc=None):
        return self.calculate_margin_impact(order, ohlc) < self.current_cash

    def execute_order(self, order, ohlc=None):

        ohlc = ohlc if ohlc is not None else self._sp.hm.get_history(order.security)[0]
        executed, price = order.test(ohlc)
        assert executed, "trying to execute order that wont execute!"

        contracts = order.num_contracts * (-1 if order.action == common.OrderAction.SELL else 1)

        self.current_cash -= contracts * price
        #TODO: fix margin stuff
        self.current_margin += self.calculate_margin_impact(order, ohlc)
        self.add_position(order.security, contracts)

    def calculate_net_position(self, order):
        pass

    def calculate_capital_impact(self, order, ohlc=None):
        # if ret > 0, you're increasing exposure. if ret < 0, you're decreasing exposure
        ohlc = ohlc if ohlc else self._sp.hm.ohlcv(order.security, 0)
        current_value = self.position_size(order.security) * ohlc.close
        executed, price = order.test(ohlc)
        order_value = price * order.num_contracts * -1 if order.action == common.OrderAction.SELL else 1
        new_value = order_value + current_value
        return abs(new_value) - abs(current_value)

    def calculate_margin_impact(self, order, ohlc=None):
        # TODO: do margin stuff here
        return self.calculate_capital_impact(order, ohlc)

