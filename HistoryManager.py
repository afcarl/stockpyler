import os
import common
import ciso8601
import pandas as pd
import feather
import json
from common import BASE_DIR

'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''


ALL_DATA_FIELDS = ['Open', 'High', 'Low', 'Close', 'Volume', 'Close_ma200']
#ALL_DATA_FIELDS = [ 'Close', 'Close_ma200']

class OHLCV:
    def __init__(self, dt, o, h, l, c, v, ma200):
        self.dt = dt
        self.open = o
        self.high = h
        self.low = l
        self.close = c
        self.volume = v
        self.ma200 = ma200

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __str__(self):
        return '{}: o:{} h: {} l: {} c: {} v:{}'.format(self.dt,self.open,self.high,self.low,self.close,self.volume)


def extend_dicts(d1, d2):
    for k,v in d2.items():
        if k not in d1:
            d1[k] = v
        else:
            d1[k].extend(v)

def slice_dicts(d, num_lines):
    for k,v in list(d.items()):
        if len(d[k]) > num_lines:
            d[k] = v[num_lines:]
        if len(d[k]) == 0:
            del d[k]


class HistoryManager:

    def __init__(self, stockpyler):
        self.enabled_securities = common.get_random_securities(1000)
        with open(os.path.join(BASE_DIR, 'security_starts_ends.json'), 'r') as f:
            secs = json.load(f)
            self.start_end_dates = dict()
            for k,v in secs.items():
                self.start_end_dates[k] = (ciso8601.parse_datetime(v[0]), ciso8601.parse_datetime(v[1]))
        self._done = False
        self._sp = stockpyler
        self.today = None
        self.trading_securities = []
        self.feeds = dict()
        self._pos = 0
        self._num_processed = 0
        self._csv_num = 0
        for thing in ALL_DATA_FIELDS:
            self.feeds[thing] = self._load_next_feather(thing)
        self._load_next_trading_securities()
        self._chunksize = 100
        self.today = self.trading_securities[0][0]

    def _load_next_feather(self, column):
        csv_file = os.path.join(BASE_DIR, 'ALL_DATA_' + column.upper() + '_' + str(self._csv_num) + '.feather')
        df = feather.read_dataframe(csv_file,columns = ['Date'] + self.enabled_securities)
        #df = pd.read_feather(csv_file,columns=['Date'] + self.enabled_securities)
        #df.set_index('Date',inplace=True,)
        ret = df.to_dict(orient='list')
        return ret

    def _load_next_trading_securities(self):
        path = os.path.join(BASE_DIR, 'TRADING_SECURITIES_' + str(self._csv_num) + '.json')
        assert os.path.exists(path)
        self.trading_securities = dict()
        with open(path, 'r') as f:
            secs = json.load(f)
            for k, v in secs.items():
                v = set(v).intersection(set(self.enabled_securities))
                self.trading_securities[ciso8601.parse_datetime(k)] = list(v)
        self.trading_securities = list(sorted(self.trading_securities.items()))

    def get_trading_securities(self):
        return self.trading_securities[self._pos][1]

    def get_num_trading_securities(self):
        return len(self.get_trading_securities())

    def start(self):
        pass

    def next(self):
        self._pos += 1
        self._num_processed += 1
        if self._pos >= self._chunksize:
            self._csv_num += 1
            self._pos -= self._chunksize
            for thing in ALL_DATA_FIELDS:
                n = self._load_next_feather(thing)
                extend_dicts(self.feeds[thing], n)
                slice_dicts(self.feeds[thing], self._chunksize)
            self._load_next_trading_securities()
        try:
            self.today =  self.trading_securities[self._pos][0]
        except:
            self._done = True

    def ohlcv(self, security, index):
        index += self._pos
        dt = self.feeds['Open']['Date'][index]
        o = self.feeds['Open'][security][index]
        h = self.feeds['High'][security][index]
        l = self.feeds['Low'][security][index]
        c = self.feeds['Close'][security][index]
        v = self.feeds['Volume'][security][index]
        ma200 = self.feeds['Close_ma200'][security][index]

        return OHLCV(dt, o, h, l, c, v, ma200)








