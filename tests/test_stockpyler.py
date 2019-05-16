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

    def stop(self):
        print("final account value", self.get_value())

    def next(self):
        print(self.today())
        trading_securities = list(self.get_trading_securities())
        print(trading_securities)
        if len(trading_securities) > 0:
            s = trading_securities[0]
            print(self._sp.hm.ohlcv(s,0))

        super().next()

#@memory_profiler.profile()
@utils.timeit
def test_stockpyler():

    all_csvs = os.listdir('C:/Users/mcdof/Documents/norgate_scraped2/us_equities/')
    random.shuffle(all_csvs)
    print(all_csvs)

    sp = Stockpyler.Stockpyler(False)

    sp.add_strategy(MyStrategy)
    sp.run()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

