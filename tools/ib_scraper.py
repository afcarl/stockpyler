from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

contract = Stock('IBM',exchange='SMART',currency='USD')
bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='30 Y',
        barSizeSetting='1 day', whatToShow='MIDPOINT', useRTH=True)

# convert to pandas dataframe:
df = util.df(bars)
print(df[['date', 'open', 'high', 'low', 'close']])