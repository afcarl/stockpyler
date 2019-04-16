# stockpyler
a python framework for systematic trading

next and _next call flow:
Stockpyler -> Strategy -> history -> feeds

all classes can be overridden, though this isnt really necessary except for strategy

The overridding class provided by the user should supply next, stop, and __init__
the backtesting framework will provide _next, _stop, etc and call these methods as necessary
