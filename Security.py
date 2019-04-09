from abc import ABC, abstractmethod

import common

class Security(ABC):

    def __init__(self, symbol, security_type, commission, commission_type, slippage, slippage_type, margin):
        self.symbol = symbol
        self.security_type = security_type
        self.commission = commission
        self.commission_type = commission_type
        self.slippage = slippage
        self.slippage_type = slippage_type
        self.margin = margin
        self._hash = None

    def __hash__(self):
        if not self._hash:
            h =  hash(self.symbol) + \
                 hash(self.security_type) + \
                 hash(self.commission) + \
                 hash(self.commission_type) + \
                 hash(self.slippage) +\
                 hash(self.slippage_type) + \
                 hash(self.margin)
            self._hash = h
        return self._hash

class Future(Security):

    def __init__(self, symbol, commission,):
        super().__init__(symbol, common.SecurityType.FUTURE, commission, common.ComissionType.PER_CONTRACT, )