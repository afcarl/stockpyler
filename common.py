from enum import Enum

class Singleton(type):
    instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class IntervalType(Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "daily"
    WEEK = "weekly"
    MONTH = "monthly"


class SecurityType(Enum):
    STOCK = "stock"
    FUTURE = "futures"
    FOREX = "forex"
    INDEX = "indices"


class ComissionType(Enum):
    NO_COMISSION = "no_comission"
    FIXED = "fixed"
    PER_CONTRACT = "per_contract"

class SlippageType(Enum):
    NO_SLIPPAGE = "no_slippage"
    FIXED = "fixed"
    PER_CONTRACT = "per_contract"
