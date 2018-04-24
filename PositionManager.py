from collections import defaultdict
from common import *
from OrderTypes import MarketOrder

def liquidating_position(action, position):
    if action == 'SELL' and position > 0:
        return True
    if action == 'BUY' and position < 0:
        return True
    return False

class PositionManager:
    #TODO: actually handle futures margins. though .1 probably isn't terrible for not trading spreads
    #Most (if not all?) requirements for fuures will be lower so let's bake in some safety
    def __init__(self, initial_capital, stock_margin = .5, future_margin = .1):
        self.capital = initial_capital
        self.margin = 0.
        self.securities = dict()

    def add_position(self, symbol, num_contracts):
        if symbol not in self.securities:
            self.securities[symbol] = 0

        self.securities[symbol] += num_contracts

        if self.securities[symbol] == 0:
            del self.securities[symbol]



    def position_size(self,symbol):
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
        o = MarketOrder(symbol, action, size)


    def liquidate_all(self):
        for symbol in self.positions():
            self.liquidate(symbol)

    def can_place_order(self, security, order):
        #TODO: futures are hard

        #we can always liquidate a position
        if self.in_position(security.symbol):
            if self.position_size(security.symbol) > 0 and order.action == 'SELL':
                return True
            if self.position_size(security.symbol) < 0 and order.action == 'BUY':
                return True

        #TODO: check available margin and stuff and do the rest of the logic

    def place_order(self, security, order):
        assert(self.can_place_order(security,order), "Placed an order when unable to do so!")

        total_price = order.price * order.num_contracts
        #TODO: adjust margin
        if liquidating_position(order.action, self.position_size(security.symbol)):
            self.capital += total_price
        else:
            self.capital -= total_price

        self.add_position(security.symbol, order.num_contracts)
