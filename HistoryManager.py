import pandas as pd
import os
import sys
import ciso8601
import utils
import datetime
import gzip
import Feed


'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''

BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/AU Equities'


class OHLCV:
    __slots__ = ['datetime', 'open', 'high', 'low', 'close', 'volume']

    def __init__(self, dt, o, h, l, c, v):
        self.datetime = dt
        self.open = o
        self.high = h
        self.low = l
        self.close = c
        self.volume = v

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __str__(self):
        return '{}: o:{} h: {} l: {} c: {} v:{}'.format(self.datetime,self.open,self.high,self.low,self.close,self.volume)

def parse_trading_securities_line(l):
    l = l.strip()
    ts, securities = l.split(' ')
    ts = ciso8601.parse_datetime(ts)
    securities = securities.split(',')
    return ts, securities

class HistoryManager(utils.NextableClass):

    def __init__(self, stockpyler):
        super().__init__()
        self._sp = stockpyler
        self.histories = dict()
        self.today = None
        self.trading_securities = []
        self.feeds = dict()
        self.txtreaders = dict()
        self._pos = 0
        self._chunksize = 10
        for thing in ['Open','High','Low','Close','Volume']:
            csv = os.path.join(BASE_DIR, 'ALL_DATA_' + thing.upper() + '.txt.gz')
            txt_reader = pd.read_csv(csv,
                        sep=',',
                        parse_dates=[0],
                        infer_datetime_format=True,
                        chunksize=self._chunksize)
            self.txtreaders[thing] = txt_reader
            self.feeds[thing] = next(txt_reader)

        self.trading_securities_file = gzip.open(os.path.join(BASE_DIR,'TRADING_SECURITIES.txt.gz'),'rt')

    def _determine_trading_securities(self):
        l = next(self.trading_securities_file)
        l = parse_trading_securities_line(l)
        #print(l)
        return l

    def get_trading_securities(self):
        return self.trading_securities

    def get_history(self, security):
        return self.histories[security]

    def get_num_trading_securities(self):
        return len(self.get_trading_securities())

    def next(self):
        self._pos += 1
        try:
            self.today, self.trading_securities = self._determine_trading_securities()
        except StopIteration:
            self._done = True

    def ohlcv(self, security, index):
        index += self._pos
        dt = self.feeds['Open']['Date'].iloc[index]
        o = self.feeds['Open'][security].iloc[index]
        h = self.feeds['High'][security].iloc[index]
        l = self.feeds['Low'][security].iloc[index]
        c = self.feeds['Close'][security].iloc[index]
        v = self.feeds['Volume'][security].iloc[index]
        return OHLCV(dt, o, h, l, c, v)








