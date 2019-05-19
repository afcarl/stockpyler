
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

        #print(self)

        super().next()

#@memory_profiler.profile()
@utils.timeit
def test_stockpyler():
    sp = Stockpyler.Stockpyler(False)

    sp.add_strategy(MyStrategy)
    sp.run()
    #ma20 = talib.MA(history.close, 20)
    #print(ma20[0])

