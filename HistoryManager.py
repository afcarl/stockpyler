import pandas as pd
import os
import sys
import csv
import ciso8601
import utils
import datetime

import gzip
import Feed

#import dask.dataframe as dd

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

    def __init__(self, path):
        super().__init__()
        self.feeds = dict()
        df = pd.read_csv(path,
                         #names=NORGATE_COLUMNS,
                         sep=',',
                         parse_dates=[0],
                         infer_datetime_format=True,
                         #date_parser=lambda x: ciso8601.parse_datetime(x),
                         usecols=NORGATE_USE_COLUMNS,)
        for column in df.columns:
            feed = Feed.Feed(df[column])
            self.feeds[column] = feed
            self.add_nextable(feed)

    def __getattr__(self, item):
        if item == '_done':
            return self._done
        elif item == 'feeds':
            return self.feeds
        return self.feeds[item]

    def __getitem__(self, item):
        feeds = self.feeds

        dt = feeds['datetime'][item]
        o = feeds['open'][item]
        h = feeds['high'][item]
        l = feeds['low'][item]
        c = feeds['close'][item]
        v = feeds['volume'][item]
        return OHLCV(dt,o,h,l,c,v)





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
        earliest = None #ciso8601.parse_datetime('9999-01-01')
        #we need to figure out all of the trading securities for all of the days we run our simulation
        for security, history in self.histories.items():
            begin_ts = history.datetime[0]
            if earliest is None or begin_ts < earliest:
                earliest = begin_ts
        self.today = earliest
        self.trading_securities = self._determine_trading_securities()

    def _determine_trading_securities(self):
        ret = []
        for security, history in self.histories.items():
            dt = history.datetime[0]
            if  dt == self.today:
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








