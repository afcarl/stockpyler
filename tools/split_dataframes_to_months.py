import os
import pandas as pd

NORGATE_COLUMNS = ['datetime','open','high','low','close','volume','turnover','aux1','aux2','aux3']


if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'

THE_DATAFRAME = pd.DataFrame({'Date': []})
THE_DATAFRAME.set_index('Date',inplace=True)

ALL_DATAFRAMES = []

first = True

subdirs = sorted(os.listdir(BASE_DIR))

SUBDIR_TO_COLS = {
    'AU Equities':['Close_ma200'],#['Open','High','Low','Close','Volume','Turnover','Unadjusted Close'],
    'AU Indices':['Close_ma200'],#['Open','High','Low','Close','Volume'],
    'AU ETOs':[],
    'AU Warrants':[],
    'Cash Commodities':['Close_ma200'],#['Open','High','Low','Close'],
    'Continuous Futures':['Close_ma200'],
    'Economic':['Close_ma200'],#['Open','High','Low','Close'],
    'Forex Spot':['Close_ma200'],#['Open','High','Low','Close'],
    'US Equities':['Close_ma200'],#['High','Low','Close','Volume','Turnover','Unadjusted Close'],
    'US Indices':['Close_ma200'],#['Open','High','Low','Close','Volume'],
    'World Indices':['Close_ma200'],#['Open','High','Low','Close','Volume'],

}

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def filter_files(f):
    valid_names = [
        'ALL_DATA_OPEN.feather',
        'ALL_DATA_HIGH.feather',
        'ALL_DATA_LOW.feather',
        'ALL_DATA_CLOSE.feather',
        'ALL_DATA_VOLUME.feather',
        'ALL_DATA_TURNOVER.feather',
        'ALL_DATA_UNADJUSTED CLOSE.feather',
        'ALL_DATA_CLOSE_MA200.feather',
    ]
    return any([f.endswith(n) for n in valid_names])

for subdir in subdirs:
    p = os.path.join(BASE_DIR,subdir)
    all_data_files = filter(filter_files, os.listdir(p))
    for d_file in all_data_files:
        fullpath = os.path.join(p,d_file)
        df = pd.read_csv(fullpath,
                         sep=',',
                         parse_dates=[0],
                         infer_datetime_format=True,
                         index_col='Date')


        list_df = [THE_DATAFRAME[i:i + 100] for i in range(0, THE_DATAFRAME.shape[0], 100)]
        p = multiprocessing.Pool(8)
        p.starmap(write_chunk, zip(list_df, itertools.repeat(out_csv), range(len(list_df))))

        for i, df in enumerate(:
            out_csv_name = fullpath.replace('.feather', "_" + str(i) + '.feather')
            if os.path.exists(out_csv_name):
                continue
            df.drop(columns=df.columns[df.isna().all()].tolist(), inplace=True)
            print(out_csv_name)
            df.to_csv(out_csv_name, float_format='%g', chunksize=100)

