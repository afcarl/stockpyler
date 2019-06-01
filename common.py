import os
from enum import Enum
import random

if os.path.isdir('/mnt/c'):
    BASE_DIR = '/mnt/c/Users/mcdof/Documents/NDExport/'
elif os.path.isdir('/home/forrest/NDExport'):
    BASE_DIR = '/home/forrest/NDExport'
elif os.path.isdir('/media/forrest/18345166345147C0/Users/mcdof/Documents/NDExport/'):
    BASE_DIR = '/media/forrest/18345166345147C0/Users/mcdof/Documents/NDExport/'
else:
    BASE_DIR = 'C:/Users/mcdof/Documents/NDExport/'


def get_all_from(base_path, ending):
    for root, dirs, files in os.walk(base_path, topdown=False):
       for name in files:
           fullpath = os.path.join(root, name)
           if fullpath.endswith(ending):
               yield fullpath

def get_random_securities(num_stocks):
    securities = list(get_all_from(os.path.join(BASE_DIR, 'US Equities'),'.feather'))
    securities = [os.path.basename(p).replace('.feather','') for p in securities]
    random.shuffle(securities)
    return securities[:num_stocks]



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
    NO_COMMISSION = "no_commission"
    FIXED = "fixed"
    PER_CONTRACT = "per_contract"

class SlippageType(Enum):
    NO_SLIPPAGE = "no_slippage"
    FIXED = "fixed"
    PER_CONTRACT = "per_contract"

class OrderExecutionStatus(Enum):
    PLACED = "order_placed"
    EXECUTED = "order_executed"
    CANCELLED = "order_cancelled"
    NOT_REJECTED = "order_rejected"
    MARGIN = 'order_margin'

class OrderAction(Enum):
    BUY = 'buy'
    SELL = 'sell'
