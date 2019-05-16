import pandas as pd
import os
NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']

def convert(path):
    df = pd.read_csv(path,
                     names=NORGATE_COLUMNS,
                     sep='\t',
                     parse_dates=[0],
                     infer_datetime_format=True,
                     memory_map=True)
    #print(df)
    df.to_csv(path, sep=',', index=False, date_format='%Y-%m-%d')


counter = 0
for root, dirs, files in os.walk("C:/Users/mcdof/Documents/norgate_scraped2", topdown=False):
    for name in files:
        fullpath = os.path.join(root, name)
        convert(fullpath)
        counter += 1
        if counter % 100 == 0:
            print(counter)