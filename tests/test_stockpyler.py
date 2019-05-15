import os
import random

import Stockpyler
import Security
import Strategy
import utils
#import memory_profiler
import talib
import pandas as pd
import Feed

BASE_PATH = 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/'

class MyStrategy(Strategy.Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ma200s = dict()
        self.max_positions = len(self._securities) / 10
        self.cur_positions = 0
        for s in self._securities:
            #self.ma200s = SimpleMovingAverage(self._histories[s],'close',200)
            series = pd.Series(self._histories[s].close._data)
            self.ma200s[s] = Feed.Feed(talib.SMA(series,200))
            self.add_indicator(s, self.ma200s[s])
            #d = np.array(self._histories[s].close._data)
            #$ma200 = Feed.Feed(ti.ema(d,256))
            #self.ma200s[s] = ma200

    def stop(self):
        print("final account value", self.get_value())



    def next(self):
        #print(self.today())
        for s in self.get_trading_securities():
            price = self._histories[s][0].close
            position = self.get_position(s)
            if price > self.ma200s[s][0] and position == 0:
                num_stocks = int(self.get_value() / price * .45)
                #print(self.today(), "buying", num_stocks, s.symbol)
                self.buy(s, num_stocks)
            elif price < self.ma200s[s][0] and position > 0:
                self.sell(s, position)
                #print(self.today(), "closing", position, s.symbol)

        super().next()

#@memory_profiler.profile()
@utils.timeit
def test_stockpyler():

    all_csvs = os.listdir('C:/Users/mcdof/Documents/norgate_scraped2/us_equities/')
    random.shuffle(all_csvs)
    print(all_csvs)

    csvs = [
        ('MO', 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/MO.txt.gz',),
        ('GE', 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/GE.txt.gz',),
    ]
    sp = Stockpyler.Stockpyler(False)

    #for csv in all_csvs[:1000]:
    #    symbol = os.path.splitext(os.path.basename(csv))[0]
    #    security = Security.Stock(symbol)
    #    history = sp.add_history(security, os.path.join(BASE_PATH,csv))

    for symbol, csv in csvs:
        security = Security.Stock(symbol)
        history = sp.add_history(security, csv)

    sp.add_strategy(MyStrategy)
    sp.run()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

