import itertools
import multiprocessing
import os
import numpy as np
import ciso8601
import struct
import pandas as pd
import csv
import time

if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
elif os.path.isdir('/home/forrest/NDExport'):
    BASE_DIR = '/home/forrest/NDExport'
elif os.path.isdir('/media/forrest/18345166345147C0/Users/mcdof/Documents/NDExport/'):
    BASE_DIR = '/media/forrest/18345166345147C0/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'

CSV_TYPES = {
    'Open':np.float64,
    'High':np.float64,
    'Low':np.float64,
    'Close':np.float64,
    'Turnover':np.float64,
    'Volume':np.float64,
    'Unadjusted Close':np.float64,
    'Close_ma200':np.float64,
    'Average_Float':np.float64,
}
HEADER_STR = 'Symbol,Open,High,Low,Close,Volume,Turnover,Unadjusted_Close,Close_ma200,Average_Float\n'

ALL_DATA_HEADER_STR = 'Date,Symbol,Open,High,Low,Close,Volume,Turnover,Unadjusted_Close,Close_ma200,Average_Float\n'

RFF_LINE_FORMAT = 'q24s12d'

def del_all_csvs():
    for thing in get_all_from(BASE_DIR, '.csv'):
        assert thing.startswith(BASE_DIR)
        assert thing.endswith('.csv')
        print("deleting",thing)
        os.remove(thing)

def get_all_from(base_path, ending, recursive=True):
    if recursive:
        for root, dirs, files in os.walk(base_path, topdown=False):
           for name in files:
               fullpath = os.path.join(root, name)
               if fullpath.endswith(ending):
                   yield fullpath
    else:
        for name in os.listdir(base_path):
            if name.endswith(ending):
                yield os.path.join(base_path,name)


def convert_to_feather(path):
    new_path = path.replace('.csv','.feather')
    #if os.path.isfile(new_path):
    #    return
    df = pd.read_csv(path)
    print("converting to feather",path)
    df.to_feather(path.replace('.csv','.feather'))


def add_indicator_column(path):
    print("writing",path)
    try:
        df = pd.read_csv(path, dtype=CSV_TYPES)
    except pd.errors.EmptyDataError:
        return
    close_ma200 = pd.DataFrame({'Close_ma200': df['Close'].rolling(200, min_periods=1).mean()})
    average_float = pd.DataFrame({'Average_Float': (df['Close'] * df['Volume']).rolling(200, min_periods=1).mean()})
    df = df.join(close_ma200)
    df = df.join(average_float)
    df.rename({'Unadjusted Close':'Unadjusted_Close'}, inplace=True, axis='columns')
    df.to_feather(path.replace('.csv', '.feather'))

def convert_all_to_feather(recursive):
    #for thing in get_all_from(BASE_DIR,'.csv',recursive):
    #    convert_to_feather(thing)
    p = multiprocessing.Pool(4)
    p.map(convert_to_feather, get_all_from(BASE_DIR,'.csv',recursive))


def gen_all_indicators():
    p = multiprocessing.Pool(4)
    #for thing in get_all_from(BASE_DIR,'.csv'):
    #    add_indicator_column(thing)
    p.map(add_indicator_column, get_all_from(BASE_DIR,'.csv'))

DATE_CSV_MAP = dict()

def _to_daily_csv(feather):
    print("splitting to daily files:",feather)
    df = pd.read_feather(feather)
    for row in df.itertuples():
        date = row.Date
        line = ','.join(str(s) for s in row[2:]) + '\n'
        fullpath = os.path.join(BASE_DIR, date + '.csv')
        DATE_CSV_MAP[fullpath].write(line)

def to_daily_csvs():
    df = pd.read_feather(os.path.join(BASE_DIR, 'USIndices', '$DJIT.feather'))
    for date in df['Date']:
        fullpath = os.path.join(BASE_DIR, date + '.csv')
        if fullpath not in DATE_CSV_MAP:
            print("opening", fullpath)
            f = open(fullpath, 'w+')
            f.write(HEADER_STR)
            DATE_CSV_MAP[fullpath] = f

    DATE_CSV_MAP['/home/forrest/NDExport/2019-05-29.csv'] = open('/home/forrest/NDExport/2019-05-29.csv','w')

    for f in get_all_from(BASE_DIR,'.feather'):
        _to_daily_csv(f)

    for f in DATE_CSV_MAP.values():
        f.close()

def _sort_by_float(path):
    df = pd.read_feather(path)
    df.sort_values('Average_Float', inplace=True, ascending=False)
    df.reset_index(inplace=True)
    df.drop(['index'], axis='columns', inplace=True)
    print("Sorting by float",path)
    df.to_feather(path)

def sort_by_float():
    #p = multiprocessing.Pool(4)
    # for thing in get_all_from(BASE_DIR,'.csv'):
    #    add_indicator_column(thing)
    #p.map(_sort_by_float, get_all_from(BASE_DIR, '.feather', False))
    for thing in get_all_from(BASE_DIR, '.feather', False):
        _sort_by_float(thing)

def concat_dailies():
    with open(os.path.join(BASE_DIR,'ALL_DATA.csv'),'w+') as out_f:
        out_f.write(ALL_DATA_HEADER_STR)
        csvs = list(sorted(get_all_from(BASE_DIR, '.csv', False)))
        for c in csvs:
            if 'ALL_DATA' in c:
                continue
            today = os.path.basename(c).replace('.csv','')
            print(c)
            with open(c, 'r') as in_f:
                #skip the header line
                next(in_f)
                for line in in_f:
                    line = today + ',' + line
                    out_f.write(line)

def all_csv_to_rff():
    with open(os.path.join(BASE_DIR,'ALL_DATA.csv'),'r') as in_f, open(os.path.join(BASE_DIR,'ALL_DATA.rff'),'wb+') as out_f:
        reader = csv.DictReader(in_f)
        last_day = None
        for row in reader:
            ts = ciso8601.parse_datetime(row['Date'])
            if ts != last_day:
                print(ts)
                last_day=ts
            r = struct.pack(RFF_LINE_FORMAT,
                        int(time.mktime(ts.timetuple())),
                        bytes(row['Symbol'].encode('utf-8')),
                        float(row['Open']),
                        float(row['High']),
                        float(row['Low']),
                        float(row['Close']),
                        float(row['Volume']),
                        float(row['Turnover']),
                        float(row['Unadjusted_Close']),
                        float(row['Close_ma200']),
                        float(row['Average_Float']),
                        0.0,
                        0.0,
                        0.0)
            out_f.write(r)
            #print(r)


def generate_trading_securities():
    subdirs = [
        'AUEquities',
        'AUIndices',
        #'AUETOs',
        #'AUWarrants',
        'CashCommodities',
        'ContinuousFutures',
        'Economic',
        'ForexSpot',
        'USEquities',
        'USIndices',
        'WorldIndices',
    ]

    all_start_end = dict()
    for d in subdirs:
        for f in os.listdir(os.path.join(BASE_DIR,d)):
            if not f.endswith('.feather'):
                continue
            stock_name = f.replace('.feather', '')
            fullpath = os.path.join(BASE_DIR,d,f)
            df = pd.read_feather(fullpath)
            start = df['Date'].iloc[0]
            end = df['Date'].iloc[-1]
            all_start_end[f] = (start, end)
            print(stock_name, start, end)
    import json
    with open(BASE_DIR + 'security_starts_ends.json', 'w+') as f:
        print("Writing",BASE_DIR + 'security_starts_ends.json')
        json.dump(all_start_end, f)


if __name__ == '__main__':
    #gen_all_indicators()
    #del_all_csvs()
    #to_daily_csvs()
    #convert_all_to_feather(False)
    #sort_by_float()
    #del_all_csvs()
    #generate_trading_securities()
    #concat_dailies()
    all_csv_to_rff()