import Stockpyler
import Security
import Strategy
import utils
import os
import talib


class MyStrategy(Strategy.Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for s in self._securities:
            ma200 = talib.MA(self._histories[s].close, 200)
            self.ma200 = ma200
            self.add_indicator(s, ma200)

    def stop(self):
        print("final account value", self.get_value())

    def next(self):
        #print(self.today())
        for s in self.get_trading_securities():
            price = self._histories[s].close[0]
            position = self.get_position(s)
            if price > self.ma200[0] and position == 0:
                num_stocks = int(self.get_value() / price * .95)
                print("buying", num_stocks)
                self.buy(s, num_stocks)
            elif price < self.ma200[0] and position > 0:
                print("closing", position)
                self.sell(s, position)

        super().next()

@utils.timeit
def test_stockpyler():
    if os.name == 'nt':
        csv_path = 'C:/Users/mcdof/Documents/norgate_scraped/us_equities/MO.txt'
    else:
        csv_path = '/mnt/c/Users/mcdof/Documents/otherdata/kibot_data/stocks/daily/HPQ.txt'
    sp = Stockpyler.Stockpyler(False)

    security = Security.Stock('HPQ')
    history = sp.add_history(security, csv_path)

    sp.add_strategy(MyStrategy)
    sp.run()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

