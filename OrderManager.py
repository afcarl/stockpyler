from abc import ABC, abstractmethod

#TODO: add time based stuff for if we want to close out positions due to too much time passing
class Order(ABC):
    @abstractmethod
    def update(self, ohlc):
        pass

    @abstractmethod
    def test(self, ohlc):
        pass

class MarketOrder(Order):

    def __init__(self, symbol, action):
        self.symbol = symbol
        self.action = action

    def update(self, ohlc):
        pass

    def test(self, ohlc):
        #Market orders always execute
        return True, ohlc.open

class LimitOrder(Order):

    def __init__(self, symbol, action, limit):
        self.symbol = symbol
        self.action = action
        self.limit = limit

    def update(self, ohlc):
        pass

    def test(self, ohlc):
        if self.action == 'BUY' and self.limit > ohlc.low:
            return True, self.limit
        elif self.action == 'SELL' and self.limit < ohlc.high:
            return True, self.limit
        return False, 0.0

class StopOrder(Order):

    def __init__(self, symbol, action, stop):
        self.symbol = symbol
        self.action = action
        self.stop = stop


    def update(self, ohlc):
        pass

    def test(self, ohlc):
        if self.action == 'BUY' and self.stop < ohlc.high:
            return True, self.stop
        elif self.action == 'SELL' and self.stop > ohlc.low:
            return True, self.stop
        return False, 0.0

class TrailOrder(Order):

    def __init__(self, symbol, action, trail_percent, price):
        self.symbol = symbol
        self.action = action,
        self.trail_percent = trail_percent
        if action == 'BUY':
            self.stop = price * (1.0 - trail_percent)
        elif action == 'SELL':
            self.stop = price * (1.0 + trail_percent)

    def update(self, ohlc):
        if self.action == 'BUY' and

class OrderManager:

    def __init__(self):
        pass

    def