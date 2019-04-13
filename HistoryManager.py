import pandas as pd
import os
import abc

from collections import namedtuple

import common
import TimeManager
import kibot
import Feed

'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''

COLUMNS = ['datetime', 'open', 'high', 'low', 'close', 'volume']

OHLC = namedtuple('OHLC', ['open','high','low','close'])

class History:
    def __init__(self, df):
        self._done=False
        self.feeds = dict()
        for name in df.columns.values.tolist():
            self.feeds[name] = Feed.Feed(df[name])

    def __getattr__(self, item):
        if item == '_done':
            return self._done
        return self.feeds[item]

    def get_ohlc(self, index):
        return OHLC(self.open, self.high, self.low, self.close)

    def _next(self):
        done = True
        for f, v in self.feeds.items():
            v.next()
            v._next()
            if not v._done:
                done = False
        self._done = done

    @abc.abstractmethod
    def next(self):
        pass

class HistoryManager:

    def __init__(self, stockpyler):
        self._sp = stockpyler
        self._done = False
        self.histories = dict()

    def add_history(self, security, path_to_file, names=None):
        if names is None:
            names = COLUMNS
        if not os.path.isfile(path_to_file):
            raise ValueError("cant open file", path_to_file)
        df = pd.read_csv(path_to_file,names=names)
        h = History(df)
        self.histories[security] = h
        return h

    def get_history(self, security):
        return self.histories[security]

    @abc.abstractmethod
    def next(self):
        pass

    def _next(self):
        done = True
        for k,v in self.histories.items():
            v.next()
            v._next()
            if not v._done:
                done = False
        self._done = done

