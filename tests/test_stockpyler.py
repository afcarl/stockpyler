import Stockpyler
import Security
import talib
import HistoryManager
import Strategy
import utils

class MyStrategy(Strategy.Strategy):

    def __init__(self, *args, **kwargs):
        #self._done
        super().__init__(*args, **kwargs)

    def next(self):
        for s in self._securities:
            self.buy(s, 1)

@utils.timeit
def test_stockpyler():

    sp = Stockpyler.Stockpyler(False)
    csv_path = 'C:/Users/mcdof/Documents/otherdata/kibot_data/stocks/daily/HPQ.txt'
    security = Security.Stock('HPQ')
    history = sp.add_history(security, csv_path)
    sp.add_strategy(MyStrategy)
    sp.run()
    ma20 = talib.MA(history.close, 20)
    print(ma20[0])

if __name__ == '__main__':
    test_stockpyler()