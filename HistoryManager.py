import pandas as pd
import os
import abc

from collections import namedtuple

import common
import TimeManager
import kibot
import Feed
import utils

'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''

COLUMNS = ['datetime', 'open', 'high', 'low', 'close', 'volume']

OHLC = namedtuple('OHLC', ['open','high','low','close'])


class History(utils.NextableClass):

    def __init__(self, df):
        super().__init__()
        self.feeds = dict()
        for name in df.columns.values.tolist():
            f = Feed.Feed(df[name])
            self.feeds[name] = f
            self.add_nextable(f)

    def __getattr__(self, item):
        if item == '_done':
            return self._done
        return self.feeds[item]

    def get_ohlc(self):
        return OHLC(self.open, self.high, self.low, self.close)

    @abc.abstractmethod
    def next(self):
        pass

class HistoryManager(utils.NextableClass):

    def __init__(self, stockpyler):
        super().__init__()
        self._sp = stockpyler
        self.histories = dict()

    def add_history(self, security, path_to_file, names=None):
        if names is None:
            names = COLUMNS
        if not os.path.isfile(path_to_file):
            raise ValueError("cant open file", path_to_file)
        df = pd.read_csv(path_to_file,names=names)
        h = History(df)
        self.histories[security] = h
        self.add_nextable(h)
        return h

    def get_history(self, security):
        return self.histories[security]

    @abc.abstractmethod
    def next(self):
        pass

