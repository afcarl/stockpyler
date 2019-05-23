import os

import pandas as pd

NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']


if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'


first = True

subdirs =  sorted(os.listdir(BASE_DIR))


for subdir in subdirs:
    all_csvs = sorted(os.listdir(os.path.join(BASE_DIR, subdir)))

    for csv in all_csvs:
        fullpath = os.path.join(BASE_DIR, subdir, csv)
        if not fullpath.endswith('csv'):
            continue
        security_name = csv.replace('.csv','')

        fullpath = os.path.join(BASE_DIR, subdir, csv)
        if 'names' in fullpath or 'ALL_DATA' in csv:
            continue
        csv_name = os.path.basename(csv).replace('.txt', '').replace('.gz', '').replace('.csv', '')
        print(fullpath)
        try:
            df = pd.read_csv(fullpath,
                         # names=['Date', 'Open', 'High', 'Low', 'Close'],
                         sep=',',
                         parse_dates=[0],
                         infer_datetime_format=True,
                         index_col='Date')
        except:
            continue
        df.to_csv(fullpath, float_format='%g')