from enum import Enum


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

def DoingBackTest():
    return True
