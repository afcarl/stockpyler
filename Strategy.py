from abc import ABC, abstractmethod
from common import *

class Strategy(ABC):


    @abstractmethod
    def update(self):
        pass

    def done(self):
        if not DoingBackTest():
            raise ValueError("Can't be done during live trading!")
        return self.done
