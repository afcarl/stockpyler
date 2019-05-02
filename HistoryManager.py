import pandas as pd
import os
import abc

from collections import namedtuple, defaultdict

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
NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']
NORGATE_USE_COLUMNS = ['datetime','open','high','low','close','volume',]

NORGATE_DTYPES = {
    'open': 'float32',
    'high': 'float32',
    'low': 'float32',
    'close': 'float32',
    'volume': 'float64',
}

OHLC = namedtuple('OHLC', ['open','high','low','close'])


class History(utils.NextableClass):

    def __init__(self, df):
        super().__init__()
        self.feeds = dict()
        for name in df.columns.values:
            f = Feed.Feed(df[name])
            self.feeds[name] = f
            self.add_nextable(f)

    def __getattr__(self, item):
        if item == '_done':
            return self._done
        return self.feeds[item]

    def get_ohlc(self):
        return OHLC(self.open, self.high, self.low, self.close)


class HistoryManager(utils.NextableClass):

    def __init__(self, stockpyler):
        super().__init__()
        self._sp = stockpyler
        self.histories = dict()
        self.days_to_securities = defaultdict(lambda: [])
        self.today = None
        self.position = 0
        self._indx = 0

    def add_history(self, security, path_to_file, names=None):
        if names is None:
            names = NORGATE_COLUMNS
        if not os.path.isfile(path_to_file):
            raise ValueError("cant open file", path_to_file)
        df = pd.read_csv(path_to_file, names=names, sep='\t', parse_dates=[0], infer_datetime_format=True, usecols=NORGATE_USE_COLUMNS)
        #if names == NORGATE_COLUMNS:
        #    df.drop(columns=['turnover', 'aux1', 'aux2', 'aux3'])
        h = History(df)
        self.histories[security] = h
        self.add_nextable(h)
        return h

    def start(self):
        #we need to figure out all of the trading securities for all of the days we run our simulation
        for security, history in self.histories.items():
            for ts in history.datetime._data:
                self.days_to_securities[ts].append(security)
        self.days_to_securities = sorted(self.days_to_securities.items())
        #for d in self.days_to_securities:
        #    print(d)
        self.today = self.days_to_securities[0][0]

    def get_trading_securities(self):
        for s in self.days_to_securities[self._indx][1]:
            yield s

    def get_history(self, security):
        return self.histories[security]

    def get_num_trading_securities(self):
        return len(self.days_to_securities[self._indx][1])

    def next(self):
        self.today = self.days_to_securities[self._indx]
        for s in self.get_trading_securities():
            self.histories[s].next()
        if self.all_children_are_done():
            self._done = True
        self._indx += 1




