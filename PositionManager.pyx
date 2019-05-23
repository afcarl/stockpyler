
import OrderTypes
import common


class PositionManager:
    def __init__(self, stockpyler, initial_cash=1000.0, stock_margin = .5):
        self.sp = stockpyler
        self.current_cash = initial_cash
        self.stock_margin = stock_margin
        self.current_margin = 0.
        self.positions = dict()

        self.orders = list()
        self.current_order_id = 0

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
        new_orders = []
        for order in self.orders:
            ohlc = self.sp.hm.ohlcv(order.security, 0)
            execute, price = order.test(ohlc)
            if execute:
                if self.can_place_order(order):
                    self.sp.pm.execute_order(order, ohlc)
                else:
                    order.status = common.OrderExecutionStatus.MARGIN
            else:
                order.update(ohlc)
                new_orders.append(order)
        self.orders = new_orders

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
        self.sp.om.simple(o)

    def liquidate_all(self):
        for security in self.get_positions():
            self.liquidate(security)

    def get_current_cash(self):
        return self.current_cash

    def get_current_margin(self):
        return self.current_margin

    def get_current_value(self):
        value = self.get_current_cash()
        for k, v in self.positions.items():
            value += self.sp.hm.ohlcv(k, 0).close * v
        return value

    def increases_exposure(self, order):
        return self.calculate_margin_impact(order) > 0

    def can_place_order(self, order, ohlc=None):
        return self.calculate_margin_impact(order, ohlc) < self.current_cash

    def execute_order(self, order, ohlc=None):

        ohlc = ohlc if ohlc is not None else self.sp.hm.get_history(order.security)[0]
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
        ohlc = ohlc if ohlc else self.sp.hm.ohlcv(order.security, 0)
        current_value = self.position_size(order.security) * ohlc.close
        executed, price = order.test(ohlc)
        order_value = price * order.num_contracts * -1 if order.action == common.OrderAction.SELL else 1
        new_value = order_value + current_value
        return abs(new_value) - abs(current_value)

    def calculate_margin_impact(self, order, ohlc=None):
        # TODO: do margin stuff here
        return self.calculate_capital_impact(order, ohlc)

