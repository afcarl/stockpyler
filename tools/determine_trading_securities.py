import os
import pandas as pd
from collections import defaultdict
import ciso8601
import pickle
import gzip
import numpy as np
NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']


if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]



TRADING_SECURITIES = defaultdict(lambda: set())
all_feathers = list(filter(lambda x: 'ALL_DATA_CLOSE_' in x, sorted(os.listdir(BASE_DIR))))

for f in all_feathers:
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

with open(os.path.join(BASE_DIR,'TRADING_SECURITIES.txt'), 'w+') as f:
    for ts, securities in sorted(TRADING_SECURITIES.items()):
        l = "{} {}\n".format(ts.strftime('%Y-%m-%d'), ','.join(sorted(securities)))
        print(l)
        f.write(l)
