import pandas as pd
import os

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
        self.feeds = dict()
        for name in df.columns.values.tolist():
            self.feeds[name] = Feed.Feed(df[name])

    def __getattr__(self, item):
        return self.feeds[item]

    def get_ohlc(self, index):
        return OHLC(self.open, self.high, self.low, self.close)

class HistoryManager:

    def __init__(self, global_manager):
        self.gm = global_manager
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


