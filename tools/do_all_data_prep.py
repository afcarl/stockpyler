import pandas as pd
import os
import multiprocessing
import itertools

if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'

def grouper_it(n, iterable):
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)

def del_all_csvs():
    for thing in get_all_from(BASE_DIR, '.csv'):
        os.remove(thing)

def get_all_from(base_path, ending):
    for root, dirs, files in os.walk(base_path, topdown=False):
       for name in files:
           fullpath = os.path.join(root, name)
           if fullpath.endswith(ending):
               yield fullpath


def convert_to_feather(path):
    try:
        #16kb is about a year of history. if we havent been trading that long then we dont want to trade them
        if os.path.getsize(path) < 16384:
            return
        df = pd.read_csv(path)
        print(path)
        df.to_feather(path.replace('.csv','.feather'))
    except:
        pass

def concat_all(column):

    THE_DATAFRAME = pd.DataFrame({'Date': []})
    THE_DATAFRAME.set_index('Date', inplace=True)

    for p in get_all_from(BASE_DIR,".feather"):
        print("reading",p)
        name = os.path.basename(p).replace('.txt', '').replace('.gz', '').replace('.csv', '').replace('.feather','')
        df = pd.read_feather(p,columns=['Date',column])
        df.set_index('Date', inplace=True)
        df.rename(lambda x: name if x != 'Date' else x, inplace=True, axis='columns')
        THE_DATAFRAME = THE_DATAFRAME.merge(df, how='outer',on='Date',)
    THE_DATAFRAME.sort_values('Date', inplace=True)
    THE_DATAFRAME.reset_index(inplace=True)
    out_name = os.path.join(BASE_DIR, 'ALL_DATA' + column.upper() + '.feather')
    print("writing",out_name)
    THE_DATAFRAME.to_feather(out_name)

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

def concat_all_columns():
    p = multiprocessing.Pool(1)
    columns = ['Open','High', 'Low', 'Close', 'Volume', 'Turnover', 'Unadjusted Close', 'Close_ma200']
    p.map(concat_all, columns)




if __name__ == '__main__':
    convert_all_to_feather()
    del_all_csvs()
    gen_all_indicators()
    concat_all_columns()