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





if __name__ == '__main__':
    test_sma()


