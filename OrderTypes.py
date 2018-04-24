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

    def __init__(self, security, action, num_contracts):
        self.security = security
        self.action = action
        self.num_contracts = num_contracts

    def update(self, ohlc):
        pass

    def test(self, ohlc):
        #Market orders always execute
        return True, ohlc.open, self.num_contracts

class LimitOrder(Order):

    def __init__(self, security, action, limit, num_contracts):
        self.security = security
        self.action = action
        self.limit = limit
        self.num_contracts = num_contracts


    def update(self, ohlc):
        pass

    def test(self, ohlc):
        if self.action == 'BUY' and self.limit > ohlc.low:
            return True, self.limit
        elif self.action == 'SELL' and self.limit < ohlc.high:
            return True, self.limit
        return False, 0.0, self.num_contracts

class StopOrder(Order):

    def __init__(self, security, action, stop, num_contracts):
        self.security = security
        self.action = action
        self.stop = stop
        self.num_contracts = num_contracts

    def update(self, ohlc):
        pass

    def test(self, ohlc):
        if self.action == 'BUY' and self.stop < ohlc.high:
            return True, self.stop
        elif self.action == 'SELL' and self.stop > ohlc.low:
            return True, self.stop
        return False, 0.0, self.num_contracts

class TrailOrder(Order):

    def __init__(self, security, action, trail_percent, price, num_contracts):
        self.security = security
        self.action = action
        self.trail_percent = trail_percent
        self.num_contracts = num_contracts

        if action == 'BUY':
            self.stop = price * (1.0 - trail_percent)
        elif action == 'SELL':
            self.stop = price * (1.0 + trail_percent)

    def update(self, ohlc):
        if self.action == 'BUY':
            self.stop = max(self.stop, ohlc.high* (1.0 - self.trail_percent))
        elif self.action == 'SELL':
            self.stop = min(self.stop, ohlc.high* (1.0 + self.trail_percent))

    def test(self, ohlc):
        if self.action == 'BUY' and self.stop < ohlc.high:
            return True, self.stop
        elif self.action == 'SELL' and self.stop > ohlc.low:
            return True, self.stop
        return False, 0.0, self.num_contracts
