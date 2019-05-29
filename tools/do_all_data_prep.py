import itertools
import multiprocessing
import os

import pandas as pd

if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'




def del_all_csvs():
    for thing in get_all_from(BASE_DIR, '.csv'):
        assert thing.startswith(BASE_DIR)
        assert thing.endswith('.csv')
        print("deleting",thing)
        os.remove(thing)

def get_all_from(base_path, ending):
    for root, dirs, files in os.walk(base_path, topdown=False):
       for name in files:
           fullpath = os.path.join(root, name)
           if fullpath.endswith(ending):
               yield fullpath


def convert_to_feather(path):
    try:
        df = pd.read_csv(path)
        print("converting",path)
        df.to_feather(path.replace('.csv','.feather'))
    except:
        pass

def add_indicator_column(path):
    try:
        print("writing",path)
        df = pd.read_feather(path)
        new_df = pd.DataFrame({'Close_ma200': df['Close'].rolling(200, min_periods=1).mean()})
        df = df.join(new_df)
        df.to_feather(path)

    except:
        pass

def convert_all_to_feather():
    p = multiprocessing.Pool(8)
    p.map(convert_to_feather, get_all_from(BASE_DIR,'.csv'))


def gen_all_indicators():
    p = multiprocessing.Pool(8)
    p.map(add_indicator_column, get_all_from(BASE_DIR,'.feather'))

def to_daily_csvs():
    DATE_CSV_MAP = dict()
    for feather in get_all_from(BASE_DIR, '.feather'):
        print(feather)
        df = pd.read_feather(feather)
        for row in df.itertuples():
            date = row.Date
            line = ','.join(str(s) for s in row[2:]) + '\n'
            fullpath = os.path.join(BASE_DIR, date + '.csv')
            if fullpath not in DATE_CSV_MAP:
                print("opening",fullpath)
                f = open(fullpath, 'w+')
                DATE_CSV_MAP[fullpath] = f
            DATE_CSV_MAP[fullpath].write(line)
            #print(fullpath)
    for f in DATE_CSV_MAP.values():
        f.close()




if __name__ == '__main__':
    #convert_all_to_feather()
    #del_all_csvs()
    #gen_all_indicators()
    to_daily_csvs()
