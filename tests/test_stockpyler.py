import Stockpyler
import Security
import Strategy
import utils
#import memory_profiler

class MyStrategy(Strategy.Strategy):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ma200s = dict()
        #for s in self._securities:
            #d = np.array(self._histories[s].close._data)
            #$ma200 = Feed.Feed(ti.ema(d,256))
            #self.ma200s[s] = ma200
            #self.add_indicator(s, ma200)

    def stop(self):
        print("final account value", self.get_value())

    def next(self):
        #print(self.today())
        for s in self.get_trading_securities():
            #print(s.symbol)
            price = self._histories[s].get(0).close
            position = self.get_position(s)
            if price > self._histories[s].get(-1).close and position == 0:
                num_stocks = int(self.get_value() / price * .45)
                #print("buying", num_stocks,s.symbol)
                self.buy(s, num_stocks)
            elif price <  self._histories[s].get(-1).close and position > 0:
                #print("closing", position,s.symbol)
                self.sell(s, position)

        super().next()

#@memory_profiler.profile()
@utils.timeit
def test_stockpyler():
    csvs = [
        ('MO', 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/MO.txt.gz',),
        ('GE', 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/GE.txt.gz',),
    ]
    sp = Stockpyler.Stockpyler(False)

    for symbol, csv in csvs:
        security = Security.Stock(symbol)
        history = sp.add_history(security, csv)

    sp.add_strategy(MyStrategy)
    sp.run()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

