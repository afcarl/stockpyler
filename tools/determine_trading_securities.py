import os
from collections import defaultdict
import json
import numpy as np
import pandas as pd
import re

NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']


if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]


all_feathers = list(filter(lambda x: 'ALL_DATA_OPEN_' in x, sorted(os.listdir(BASE_DIR),key=natural_sort_key)))
print(all_feathers)
with open(os.path.join(BASE_DIR,'TRADING_SECURITIES.txt'), 'w+') as out_f:
    for f in all_feathers:
        TRADING_SECURITIES = defaultdict(lambda: set())
        fullpath = os.path.join(BASE_DIR, f)
        print("reading", fullpath)
        security_name = f.replace('.feather', '')
        df = pd.read_feather(fullpath)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        thing = df.to_dict()
        for stock, v in thing.items():
            for date, value in v.items():
                if not np.isnan(value):
                    TRADING_SECURITIES[date].add(stock)
        for ts, securities in sorted(TRADING_SECURITIES.items()):
            securities = list(sorted(securities))
            securities_str = json.dumps(securities)
            l = "{} {}\n".format(ts.strftime('%Y-%m-%d'), securities_str)
            out_f.write(l)

