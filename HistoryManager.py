import pandas as pd
import os
import sys
import csv
import ciso8601
import utils
import datetime

import gzip

'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''

COLUMNS = ['datetime', 'open', 'high', 'low', 'close', 'volume']
NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']
NORGATE_USE_COLUMNS = ['datetime','open','high','low','close','volume',]


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


class History(utils.NextableClass):

    def __init__(self, path, chunksize=1000):
        super().__init__()
        self._chunksize = chunksize
        self._file = gzip.open(path, 'rt')
        self._csvreader = csv.reader(self._file, delimiter=',')
        self.rows = []
        self.pos = 0
        #skip the header because we hardcode that shit
        next(self._csvreader)
        #we might need to get the 0th row before start is called, so do it here
        #and do nothing in start
        self.rows.append(self.parse_row(next(self._csvreader)))

    def parse_row(self, row):
        dt = ciso8601.parse_datetime(row[0])
        o, h, l, c, v = float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])
        return OHLCV(dt, o, h, l, c, v)


    def next(self):
        try:
            cur_row = self.parse_row(next(self._csvreader))
        except StopIteration:
            self._done = True
            return
        self.rows.append(cur_row)
        self.pos += 1
        if len(self.rows) == 2000:
            self.rows = self.rows[1000:]
            self.pos -= 1000

    def __getitem__(self, item):
        if isinstance(item,slice):
            assert item.start < 0, "Only support slices from the end of the history"
            return self.rows[item]
        else:
            assert item <= 0, "Can't look into the future!"
            # TODO: what to do about reading before start / after end?
            # have considered negative indicies to return the 0th element, and > len(this) indicies to return the last element
            # TODO: lazy load in/out so we hopefully dont take infinity ram
            index = item + self.pos
            return self.rows[index]


    def __del__(self):
        self._file.close()


class HistoryManager(utils.NextableClass):

    def __init__(self, stockpyler):
        super().__init__()
        self._sp = stockpyler
        self.histories = dict()
        self.today = None
        self.trading_securities = []

    def add_history(self, security, path_to_file, names=None):
        if names is None:
            names = NORGATE_COLUMNS
        if not os.path.isfile(path_to_file):
            raise ValueError("cant open file", path_to_file)

        h = History(path_to_file)
        self.histories[security] = h
        self.add_nextable(h)
        return h

    def start(self):
        earliest = ciso8601.parse_datetime('9999-01-01')
        #we need to figure out all of the trading securities for all of the days we run our simulation
        for security, history in self.histories.items():
            begin_ts = history[0].datetime
            if begin_ts < earliest:
                earliest = begin_ts
        self.today = earliest
        self.trading_securities = self._determine_trading_securities()

    def _determine_trading_securities(self):
        ret = []
        for security, history in self.histories.items():
            if history[0].datetime == self.today:
                ret.append(security)
        return ret

    def get_trading_securities(self):
        return self.trading_securities

    def get_history(self, security):
        return self.histories[security]

    def get_num_trading_securities(self):
        return len(self.get_trading_securities())

    def next(self):
        for s in self.get_trading_securities():
            self.histories[s].next()
        if self.all_children_are_done():
            self._done = True
        self.today += datetime.timedelta(days=1)
        self.trading_securities = self._determine_trading_securities()








