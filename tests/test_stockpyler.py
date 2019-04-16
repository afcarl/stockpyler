import Stockpyler
import Security
import Strategy
import utils
import os


class MyStrategy(Strategy.Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_buy_calls = 0

    def next(self):
        #print(self.get_value())
        for s in self._securities:
            self.num_buy_calls += 1

            #print(self.get_position(s),"buying ", s.symbol)
            self.buy(s, 1)

@utils.timeit
def test_stockpyler():
    if os.name == 'nt':
        csv_path = 'C:/Users/mcdof/Documents/otherdata/kibot_data/stocks/daily/HPQ.txt'
    else:
        csv_path = '/mnt/c/Users/mcdof/Documents/otherdata/kibot_data/stocks/daily/HPQ.txt'
    sp = Stockpyler.Stockpyler(False)

    security = Security.Stock('HPQ')
    history = sp.add_history(security, csv_path)
    sp.add_strategy(MyStrategy)
    sp.run()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

