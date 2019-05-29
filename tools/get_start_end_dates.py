import os
import pandas as pd
if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'

subdirs = [
    'AU Equities',
    'AU Indices',
    'AU ETOs',
    'AU Warrants',
    'Cash Commodities',
    'Continuous Futures',
    'Economic',
    'Forex Spot',
    'US Equities',
    'US Indices',
    'World Indices',
]

all_start_end = dict()

for d in subdirs:
    feathers = os.listdir(os.path.join(BASE_DIR,d))
    print(list(feathers))
    for f in feathers:
        stock_name = f.replace('.feather','')
        fullpath = os.path.join(BASE_DIR,d,f)
        try:
            df = pd.read_feather(fullpath)
        except:
            pass
        start = df['Date'].iloc[0]
        end = df['Date'].iloc[-1]
        all_start_end[stock_name] = (start,end)
        print(fullpath,start,end)
print(len(all_start_end))
import json
with open('/mnt/c/Users/mcdof/Documents/NDExport/security_starts_ends.json', 'w+') as f:
    json.dump(all_start_end,f)