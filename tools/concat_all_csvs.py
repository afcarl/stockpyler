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

subdirs =  sorted(os.listdir(BASE_DIR))

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

for subdir in subdirs:
    for col in SUBDIR_TO_COLS[subdir]:
        THE_DATAFRAME = pd.DataFrame({'Date': []})
        THE_DATAFRAME.set_index('Date', inplace=True)
        all_csvs = sorted(os.listdir(os.path.join(BASE_DIR,subdir)))
        chunked = chunks(all_csvs,1000)
        for sublist in chunked:
            dfs = []

            for csv in sublist:
                fullpath = os.path.join(BASE_DIR, subdir, csv)
                if 'names' in fullpath or 'ALL_DATA' in csv:
                    continue
                csv_name = os.path.basename(csv).replace('.txt', '').replace('.gz', '').replace('.csv', '')
                print(fullpath)
                try:
                    df = pd.read_csv(fullpath,
                                     #names=['Date', 'Open', 'High', 'Low', 'Close'],
                                     sep=',',
                                     parse_dates=[0],
                                     infer_datetime_format=True, index_col='Date',
                                     usecols=['Date', col])
                except:
                    continue
                if len(df) < 5:
                    continue
                print(len(df))
                df.rename(lambda x: csv_name if x != 'Date' else x, inplace=True, axis='columns')
                dfs.append(df)
            THE_DATAFRAME = THE_DATAFRAME.join(dfs, how='outer')
        THE_DATAFRAME.sort_values('Date', inplace=True)
        out_csv = os.path.join(BASE_DIR, subdir, 'ALL_DATA_' + col.upper() + '.txt')
        print("writing", out_csv)
        list_df = [THE_DATAFRAME[i:i + 100] for i in range(0, THE_DATAFRAME.shape[0], 100)]
        list_df[0].to_csv(out_csv, float_format='%g', chunksize=100)
        for l in list_df[1:]:
            l.to_csv(out_csv, float_format='%g', chunksize=100, mode='a',header=False)


'''
for csv in sorted(os.listdir(BASE_DIR)):
    if 'names' in csv or 'ALL_DATA' in csv:
        continue
    csv_name = os.path.basename(csv).replace('.txt', '').replace('.gz', '').replace('.csv','')
    print(csv_name)
    fullpath = os.path.join(BASE_DIR,csv)
    df = pd.read_csv(fullpath,
                     names = ['Date','open','high','low','close','volume','turnover','adj_close'],
                     sep=',',
                     parse_dates=[0],
                     infer_datetime_format=True,index_col='Date',
                     usecols=['Date','close'])
    #df.set_index('Date',inplace=True)
    df.rename(lambda x:  csv_name if x != 'Date' else x,inplace=True, axis='columns')
    THE_DATAFRAME = THE_DATAFRAME.join(df, how='outer', on='Date')
    #THE_DATAFRAME = THE_DATAFRAME.join(df,rsuffix='_' + csv_name,how='outer',on='Date')

THE_DATAFRAME.sort_values('Date',inplace=True)
THE_DATAFRAME.to_csv(os.path.join(BASE_DIR,'ALL_DATA.txt'))
'''