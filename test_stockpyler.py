#import pyximport
#pyximport.install(language_level=3)

import Stockpyler
import Strategy
import utils
import Observer

class MyStrategy(Strategy.Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_positions = 3
        self.cur_positions = 1

    def stop(self):
        pass
        #print("final account value", self.get_value())

    def next(self):
        print(self.today())


        super().next()

    def sort_by_float(self, security, index):
        ohlcv = self.ohlvc(security, index)
        return ohlcv.volume * ohlcv.close

@utils.timeit
def test_stockpyler():
    sp = Stockpyler.Stockpyler(False)

    sp.add_strategy(MyStrategy)
    sp.add_observer(Observer.AccountValueObserver)
    sp.run()
    sp.show()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

