import Stockpyler
import Security
import Indicators
import talib

def test_sma():
    csvs = [
        #('MO', 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/MO.txt.gz',),
        ('GE', 'C:/Users/mcdof/Documents/norgate_scraped2/us_equities/GE.txt.gz',),
    ]
    sp = Stockpyler.Stockpyler(False)

    for symbol, csv in csvs:
        security = Security.Stock(symbol)
        history = sp.add_history(security, csv)
        data1 = history.close._data['close']
        data2 = next(history.close._chunks)
        data2 = data2['close']
        sma = data1.rolling(200, min_periods=1).mean()
        #print(sma)
        i = 0
        iter = sma.iteritems()
        while True:
            i += 1
            t = next()
            if i == 500:
                sma = sma.append(data2, ignore_index=True, verify_integrity=True)
            print(i,t)




if __name__ == '__main__':
    test_sma()


