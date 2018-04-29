import common
import datetime

class TimeManager():

    def __init__(self, global_manager):
        self.gm = global_manager
        self.history_position = 0

    def get_current_time(self):
        if self.gm.doing_backtest():
            return self.history_position
        else:
            return datetime.datetime.now()

    def advance_time(self):
        assert self.gm.doing_backtest()
        self.history_position += 1
