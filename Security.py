from abc import ABC, abstractmethod
from common import *
from DataManager import DataManager

class Security(ABC):

    def __init__(self, symbol, security_type, commission, commission_type, slippage, slippage_type):
        self.symbol = symbol
        self.security_type = security_type
        self.commission = commission
        self.commission_type = commission_type
        self.slippage = slippage
        self.slippage_type = slippage_type

