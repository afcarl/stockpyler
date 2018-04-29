from abc import ABC, abstractmethod


class Strategy(ABC):

    def __init__(self, global_manager):
        self.gm = global_manager

    @abstractmethod
    def update(self):
        pass

    def done(self):
        if not self.gm.tm.doing_backtest():
            raise ValueError("Can't be done during live trading!")
        return self.done
