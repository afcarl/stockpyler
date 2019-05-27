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
        securities = sorted(self.get_trading_securities(),key=lambda x: self.sort_by_float(x,0))
        for s in securities:
            ohlcv = self.ohlvc(s, 0)

            if ohlcv.close > ohlcv.ma200 and self.get_position(s) == 0 and self.cur_positions < self.max_positions:
                c = self.get_cash()
                num_stocks = int(self.get_cash() / self.get_num_trading_securities() / ohlcv.close *.9)
                self.cur_positions+=1
                self.buy(s,num_stocks)
            elif ohlcv.close < ohlcv.ma200 and self.get_position(s) > 0:
                self.cur_positions-=1
                self.sell(s, self.get_position(s))
        print(len(securities))
        #securities = sorted(securities, key=lambda x: self.sort_by_float(x,0))
        #print(securities)
        #print(self)

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

