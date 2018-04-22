from Strategy import Strategy
import talib

'''MACrossoverStrategy

params:
fast_period
slow_period
trend_period
stop_percent
trail_percent
profit_percent

'''

class MACrossoverStrategy(Strategy):

    def __init__(self, security, fast_period, slow_period, trend_period, stop_percent, trail_percent, profit_percent):
        self.security = security
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.trend_period = trend_period
        self.stop_percent = stop_percent
        self.trail_percent = trail_percent
        self.profit_percent = profit_percent
        self.done = False

    def update(self):
        if len(self.security.get_latest()) == 0:
            self.done = True
            return

        fast_ema = talib.EMA(self.security.get_latest(self.fast_period), self.fast_period)
        slow_ema = talib.EMA(self.security.get_latest(self.slow_period), self.slow_period)
        trend_sma = talib.MA(self.security.get_latest(self.trend_period), self.trend_period)

        prev_fast_ema = talib.EMA(self.security.get_latest(self.fast_period, 1), self.fast_period)
        prev_slow_ema = talib.EMA(self.security.get_latest(self.slow_period, 1), self.slow_period)
        prev_trend_sma = talib.MA(self.security.get_latest(self.trend_period, 1), self.trend_period)

        if fast_ema > slow_ema and prev_slow_ema > prev_fast_ema and trend_sma > prev_trend_sma:
            #go long
            pass
        if fast_ema < slow_ema and prev_slow_ema < prev_fast_ema and trend_sma < prev_trend_sma:
            #go short
            pass
