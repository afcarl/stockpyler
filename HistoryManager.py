import common
import TimeManager
import kibot

'''HistoryManager

In the interest of time vs space, eventually this will do something more complex for dealing with
multi security portfolio backtesting. until then, try not to add too many

'''
class HistoryManager():

    def __init__(self, global_manager):
        self.gm = global_manager
        self.histories = dict()

    def get_history(self, security, interval, interval_type, period, offset=0):
        assert self.gm.tm.doing_backtest()
        assert offset > 0

        begin = self.gm.tm.get_current_time() - period - offset
        if begin < 0:
            begin = 0
        end = self.gm.tm.get_current_time() - offset
        if end < begin:
            end = begin + 1

        k = (security, interval, interval_type)
        if k not in self.histories:
            self.histories[k] = kibot.KibotApi().request(security.symbol, security.security_type, interval, interval_type, period)

        return self.histories[k][begin: end]

