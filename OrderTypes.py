from abc import ABC, abstractmethod

#TODO: add time based stuff for if we want to close out positions due to too much time passing
class Order(ABC):

    def __init__(self, security, action, num_contracts):
        self.id = None
        self.status = None
        self.security = security
        self.action = action
        self.num_contracts = num_contracts
        assert num_contracts > 0, "cant buy or sell negative number of contracts!"

    @abstractmethod
    def update(self, ohlc):
        pass

    @abstractmethod
    def test(self, ohlc):
        pass


class MarketOrder(Order):

    def __init__(self, security, action, num_contracts, execute_on_close=True):
        super().__init__(security, action, num_contracts)
        #TODO: this framework assumes that the time between choosing to make a order and
        #actually making said order is small, so we execute on the close rather than waiting
        #for the next open
        #Eventually we can break that, but later
        self.execute_on_close = execute_on_close

    def update(self, ohlc):
        pass

    def test(self, ohlc):
        #Market orders always execute
        return True, ohlc.close[0]


class LimitOrder(Order):

    def __init__(self, security, action, num_contracts, limit):
        super().__init__(security, action, num_contracts)
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

    def __init__(self, security, action, num_contracts, stop):
        super().__init__(security, action, num_contracts)
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

    def __init__(self, security, action, num_contracts, trail_percent, price):
        super().__init__(security, action, num_contracts)
        self.trail_percent = trail_percent

        if action == 'BUY':
            self.stop = price * (1.0 - trail_percent)
        elif action == 'SELL':
            self.stop = price * (1.0 + trail_percent)

    def update(self, ohlc):
        if self.action == 'BUY':
            self.stop = max(self.stop, ohlc.high * (1.0 - self.trail_percent))
        elif self.action == 'SELL':
            self.stop = min(self.stop, ohlc.high * (1.0 + self.trail_percent))

    def test(self, ohlc):
        if self.action == 'BUY' and self.stop < ohlc.high:
            return True, self.stop
        elif self.action == 'SELL' and self.stop > ohlc.low:
            return True, self.stop
        return False, 0.0
