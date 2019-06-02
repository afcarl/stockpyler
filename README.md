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

bytes 0-7 - 64 bit int timestamp
bytes 8-31 - 23 bytes + '\0' for name
bytes 32-39 - open - f64
bytes 40-47 - high - f64
bytes 48-55 - low - f64
bytes 56-63 - close - f64
bytes 64-71 - volume - f64
bytes 72-79 - turnover - f64
bytes 80-87 - unadjusted_close - f64
bytes 88-95 - ma_200 - f64
bytes 96-103 - average_float - f64
bytes 104 - 111 - padding
bytes 112 - 120 - padding
bytes 121 - 128 - padding