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

BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/World Indices'


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

def parse_data_line(l):
    l = l.strip().split(',')
    return l[0],l[1:]

def read_more_lines(f, num_lines):
    ret = []
    try:
        for x in range(0,num_lines):
            l = next(f)
            ret.append(parse_data_line(l))
        return ret
    except StopIteration:
        return ret

class HistoryManager(utils.NextableClass):

    def __init__(self, stockpyler):
        super().__init__()
        self._sp = stockpyler
        self.histories = dict()
        self.today = None
        self.trading_securities = []
        self.feeds = dict()
        self.txtreaders = dict()
        self.txtreader_columns = dict()
        self._pos = 0
        self._num_processed = 0
        self._chunksize = 100
        for thing in ['Open','High','Low','Close','Volume']:
            csv = os.path.join(BASE_DIR, 'ALL_DATA_' + thing.upper() + '.txt.gz')
            txt_reader = gzip.open(csv, 'rt')
            headers = next(txt_reader).strip()
            self.txtreader_columns[thing] = headers.split(',')
            print(self.txtreader_columns)
            #for line in txt_reader:
            #    print(line)
            self.txtreaders[thing] = txt_reader
            self.feeds[thing] = read_more_lines(self.txtreaders[thing],self._chunksize)
        #todo: assert that the headers for each open/high/low etc are the same so we only actually need to store one
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
        self._num_processed += 1
        if self._pos >= self._chunksize:
            self._pos -= self._chunksize
            for thing in ['Open', 'High', 'Low', 'Close', 'Volume']:
                n = read_more_lines(self.txtreaders[thing],self._chunksize)

                self.feeds[thing].extend(n)
                self.feeds[thing] = self.feeds[thing][self._chunksize:]
        try:
            self.today, self.trading_securities = self._determine_trading_securities()
        except StopIteration:
            self._done = True

    def ohlcv(self, security_index, index):
        #index += self._pos
        index = 0
        print("accessing",index)
        dt = self.feeds['Open'][0][index]
        o = self.feeds['Open'][security_index][index]
        h = self.feeds['High'][security_index][index]
        l = self.feeds['Low'][security_index][index]
        c = self.feeds['Close'][security_index][index]
        v = self.feeds['Volume'][security_index][index]
        return OHLCV(dt, o, h, l, c, v)








