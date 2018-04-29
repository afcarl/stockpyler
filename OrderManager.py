import common
import OrderTypes
import DataManager
import PositionManager


class OrderManager:

    def __init__(self, global_manager):
        self.gm = global_manager
        self.orders = dict()
        self.current_id = 0

    def simple(self, order):
        assert(isinstance(order,OrderTypes.MarketOrder), "Only simple market orders are supported")

    def one_cancels_other(self, order1, order2):
        assert(False, "Currently only simple market orders are supported")
        self.one_cancels_all(order1, order2)

    def one_cancels_all(self, *orders):
        assert(False, "Currently only simple market orders are supported")
        ids = [self.next_id() for _ in orders]

        for id, order in zip(ids, orders):
            if not self.gm.pm.can_place_order(order):
                return common.OrderExecutionType.ORDER_NOT_PLACED
            order.id = id
            order.cancels = list(filter(lambda x: x != id, ids))
            self.orders[id] = order

        return common.OrderExecutionType.ORDER_PLACED

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def update(self, interval, interval_type):
        for key, order in self.orders.items():
            ohlc = self.gm.dm.get_latest(order.security, interval, interval_type)
            execute, price = order.test(ohlc)
            if execute:
                self.gm.pm.execute_order(order)
                del self.orders[key]
            else:
                order.update(ohlc)
