import common
import datetime

class TimeManager(metaclass=common.Singleton):

    def __init__(self):
        self.live = False
        self.history_position = 0

    def doing_backtest(self):
        return not self.live

    def get_current_time(self):
        if self.doing_backtest():
            return self.history_position
        else:
            return datetime.datetime.now()

    def advance_time(self):
        assert self.doing_backtest()
        self.history_position += 1