import os
import pandas as pd
from collections import defaultdict
import ciso8601
import pickle
import gzip
NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']


BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'

first = True

subdirs =  sorted(os.listdir(BASE_DIR))


for subdir in subdirs:
    TRADING_SECURITIES = dict()
    all_csvs = sorted(os.listdir(os.path.join(BASE_DIR, subdir)))

    for csv in all_csvs:
        fullpath = os.path.join(BASE_DIR, subdir, csv)
        if not fullpath.endswith('csv'):
            continue
        security_name = csv.replace('.csv','')
        with open(fullpath,'r') as f:
            for line in f:
                line = line.strip()
                dt = line.split(',')[0]
                try:
                    dt = ciso8601.parse_datetime(dt)
                except:
                    #this must be the column names. so skip them
                    continue
                if dt not in TRADING_SECURITIES:
                    TRADING_SECURITIES[dt] = []
                TRADING_SECURITIES[dt].append(security_name)
                #print(dt,security_name)

    for k,v in list(sorted(TRADING_SECURITIES.items())):
        print(k,v[0])
    pickle_path = os.path.join(BASE_DIR,subdir,'TRADING_SECURITIES.pickle.gz')
    print("pickle path",pickle_path)

    with gzip.open(pickle_path, 'wb+') as f:
        pickle.dump(list(sorted(TRADING_SECURITIES.items())), f)

with gzip.open('C:/Users/mcdof/Documents/NDExport/US Equities/TRADING_SECURITIES.pickle.gz', 'rb') as f:
    trading_securities = pickle.load(f)

    for thing in trading_securities:
        print(thing)