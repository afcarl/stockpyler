import os
import pandas as pd
if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
elif os.path.isdir('/home/forrest/NDExport'):
    BASE_DIR = '/home/forrest/NDExport'
elif os.path.isdir('/media/forrest/18345166345147C0/Users/mcdof/Documents/NDExport/'):
    BASE_DIR = '/media/forrest/18345166345147C0/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'



for d in subdirs:
    feathers = os.listdir(os.path.join(BASE_DIR,d))
    print(list(feathers))
    for f in feathers:
        stock_name = f.replace('.feather','')
        fullpath = os.path.join(BASE_DIR,d,f)
        df = pd.read_feather(fullpath)
        start = df['Date'].iloc[0]
        end = df['Date'].iloc[-1]
        all_start_end[stock_name] = (start,end)
        print(fullpath,start,end)
print(len(all_start_end))
import json
with open(BASE_DIR + 'security_starts_ends.json', 'w+') as f:
    json.dump(all_start_end,f)