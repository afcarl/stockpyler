# stockpyler
a python framework for systematic trading

next and _next call flow:
Stockpyler -> Strategy -> history -> feeds

all classes can be overridden, though this isnt really necessary except for strategy

The overridding class provided by the user should supply next, stop, and __init__
the backtesting framework will provide _next, _stop, etc and call these methods as necessary

data format:

*.rff (Real Fucking Fast row column data)

Everthing is little endian unless otherwise stated

bytes 0 - 3: 
  * 0 - '.'
  * 1 - 'r'
  * 2 - 'f'
  * 3 - 'f'
  
* bytes 4-7 : reserved
* bytes 8 - 15: int64_t num rows (does NOT include a row for "column names")
* bytes 16 - 23: int64_t num columns (including "key" column)
* bytes 24 - 32: int64_t offset into file of start of row data
* bytes 33 - 40: reserved
* bytes 41 - 48: reserved
* bytes 49 - 127: reserved
* bytes 128 - 128 + 32*num columns: columns names entries
  * each entry is a 32 byte c string for max 31 characters + terminating '\0'
  * Date column should be the 0th entry
* row data start
  * must be 128 byte aligned
  * row[0] is int64 datetime
  * row[1] is float64 value for first columns that isn't Date
  * row[2] etc...