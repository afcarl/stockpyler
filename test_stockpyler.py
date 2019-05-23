import pyximport
pyximport.install(language_level=3)

import Stockpyler
import Strategy
import utils
BASE_PATH = 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/'


class MyStrategy(Strategy.Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ma200s = dict()
        self.max_positions = 50
        self.cur_positions = 0

    def stop(self):
        print("final account value", self.get_value())

    def next(self):
        print(self.today())
        securities = self.get_trading_securities()
        print(len(securities))
        #securities = sorted(securities, key=lambda x: self.sort_by_float(x,0))
        #print(securities)
        #print(self)

        super().next()

    def sort_by_float(self, security, index):
        ohlcv = self.ohlvc(security, index)
        return ohlcv.volume * ohlcv.close

#@memory_profiler.profile()
@utils.timeit
def test_stockpyler():
    sp = Stockpyler.Stockpyler(False)

    sp.add_strategy(MyStrategy)
    sp.run()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

