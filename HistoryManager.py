import os
import common
import ciso8601
import pandas as pd
import feather
import json
import mmap
from common import BASE_DIR
import datetime

'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''

def feather_name(today):
    return os.path.join(BASE_DIR, today.strftime('%Y-%m-%d') + '.feather')

class HistoryManager:

    def __init__(self, stockpyler):
        self.enabled_securities = common.get_random_securities(1000)
        with open(os.path.join(BASE_DIR, 'security_starts_ends.json'), 'r') as f:
            secs = json.load(f)
            self.start_end_dates = dict()
            for k,v in secs.items():
                self.start_end_dates[k] = (ciso8601.parse_datetime(v[0]), ciso8601.parse_datetime(v[1]))
        self._done = False
        self._earliest = ciso8601.parse_datetime('9999-01-01')
        self._latest = ciso8601.parse_datetime('0001-01-01')
        for k,v in self.start_end_dates.items():
            start = v[0]
            end = v[1]
            if start < self._earliest:
                self._earliest = start
            if end > self._latest:
                self._latest = end
        self._sp = stockpyler
        self.today = self._earliest
        self._num_processed = 0
        self._load_next_feather()

    def _load_next_feather(self):
        f = open(feather_name(self.today), 'r')
        handle = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
        self._mmap_handle = handle
        self._feather_handle = f
        return feather.read_dataframe(handle)

    def start(self):
        pass

    def next(self):
        self._num_processed += 1
        self.today += datetime.timedelta(days=1)
        while not os.path.isfile(feather_name(self.today)):
            self.today += datetime.timedelta(days=1)
            if self.today > self._latest:
                self._done = True
                return
        self._mmap_handle.close()
        self._feather_handle.close()
        self.df = self._load_next_feather()


