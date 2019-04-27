from abc import ABC, abstractmethod

import common
import utils


class Security(utils.FrozenClass):

    def __init__(self, symbol, security_type, commission, commission_type, slippage, slippage_type, margin):
        super().__init__()
        self.symbol = symbol
        self.security_type = security_type
        self.commission = commission
        self.commission_type = commission_type
        self.slippage = slippage
        self.slippage_type = slippage_type
        self.margin = margin
        self._hash = hash(symbol) + \
                        hash(security_type) + \
                        hash(commission) + \
                        hash(commission_type) + \
                        hash(slippage) +\
                        hash(slippage_type) + \
                        hash(margin)

        self._freeze()


    def __hash__(self):
        return self._hash


#TODO: rather than make these default arguments, make them default=None, then have the default values configured
#through stockpyler class which will go and fill it in itself
class Future(Security):

    def __init__(self, symbol, commission, slippage, margin):
        super().__init__(symbol,
                         common.SecurityType.FUTURE,
                         commission,
                         common.ComissionType.PER_CONTRACT,
                         slippage,
                         common.SlippageType.PER_CONTRACT,
                         margin)


class Stock(Security):

    def __init__(self, symbol, commission=.005, commission_type=common.ComissionType.PER_CONTRACT, slippage=0):
        super().__init__(symbol,
                         common.SecurityType.STOCK,
                         commission,
                         commission_type,
                         slippage,
                         common.SlippageType.PER_CONTRACT,
                         None)
