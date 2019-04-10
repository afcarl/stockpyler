import Stockpyler
import Security
import talib
import HistoryManager

sp = Stockpyler.Stockpyler(False)
csv_path = 'C:/Users/mcdof/Documents/otherdata/kibot_data/stocks/daily/HPQ.txt'
security = Security.Stock('HPQ')
history = sp.add_history(security, csv_path)
ma20 = talib.MA(history.close, 20)
print(ma20[0])