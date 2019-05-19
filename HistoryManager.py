import os
import ciso8601
import sys
import utils
import csv
import pandas as pd

'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''
if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/AU Equities'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/AU Equities'

ALL_DATA_FIELDS = ['Open', 'High', 'Low', 'Close', 'Volume', 'Close_ma200']
#ALL_DATA_FIELDS = [ 'Close', 'Close_ma200']

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


class HistoryManager(utils.NextableClass):

    def __init__(self, stockpyler):
        super().__init__()
        self._sp = stockpyler
        self.today = None
        self.trading_securities = []
        self.feeds = dict()
        self._pos = 0
        self._num_processed = 0
        self._csv_num = 0
        for thing in ALL_DATA_FIELDS:
            self.feeds[thing] = self._load_next_csv(thing)
        self._chunksize = len(self.feeds['Open']['Date'])
        self.trading_securities_file = open(os.path.join(BASE_DIR, 'TRADING_SECURITIES.txt'), 'rt')
        self.today, self.trading_securities = self._determine_trading_securities()

    def _load_next_csv(self, column):
        csv_file = os.path.join(BASE_DIR, 'ALL_DATA_' + column.upper() + '_' + str(self._csv_num) + '.txt')
        with open(csv_file, 'rt') as f:
            txt_reader = csv.DictReader(f)
            ret = {col: [None]*100 for col in txt_reader.fieldnames}
            for i, line in enumerate(txt_reader):
                line['Date'] = ciso8601.parse_datetime(line['Date'])
                for k, v in line.items():
                    ret[k][i] = v
            return ret

    def _determine_trading_securities(self):
        line = next(self.trading_securities_file)
        line = parse_trading_securities_line(line)
        return line

    def get_trading_securities(self):
        return self.trading_securities

    def get_num_trading_securities(self):
        return len(self.get_trading_securities())

    def next(self):
        self._pos += 1
        self._num_processed += 1
        if self._pos >= self._chunksize:
            self._csv_num += 1
            self._pos -= self._chunksize
            for thing in ALL_DATA_FIELDS:
                n = self._load_next_csv(thing)
                extend_dicts(self.feeds[thing], n)
                slice_dicts(self.feeds[thing], self._chunksize)
                pass
        try:
            self.today, self.trading_securities = self._determine_trading_securities()
        except StopIteration:
            self._done = True

    def ohlcv(self, security, index):
        index += self._pos
        dt = self.feeds['Open']['Date'][index]
        o = self.feeds['Open'][security][index]
        h = self.feeds['High'][security][index]
        l = self.feeds['Low'][security][index]
        c = self.feeds['Close'][security][index]
        v = self.feeds['Volume'][security][index]

        return OHLCV(dt, o, h, l, c, v)








