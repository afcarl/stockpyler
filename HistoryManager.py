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
        return OHLCV(dt, o, h, l, c, v)


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
        for thing in ['Open','High','Low','Close']:
            csv = os.path.join(BASE_DIR, 'ALL_DATA_' + thing.upper() + '.txt.gz')
            txt_reader =  pd.read_csv(csv,
                        sep=',',
                        parse_dates=[0],
                        infer_datetime_format=True,
                        chunksize=10)
            self.txtreaders[thing] = txt_reader
            self.feeds[thing] = next(txt_reader)


    def _determine_trading_securities(self):
        ret = []
        for v in self.feeds['Close'].iloc[self._pos]:
            if v
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
        if len(self.get_trading_securities()) > 0:
            if self.all_children_are_done():
                self._done = True
        self.today += datetime.timedelta(days=1)
        self.trading_securities = self._determine_trading_securities()








