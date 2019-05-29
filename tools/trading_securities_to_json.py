import os
import ciso8601
import json
from common import BASE_DIR
import pandas as pd

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def parse_trading_securities_line(l):
    l = l.strip()
    ts, securities = l.split(' ', 1)
    securities = json.loads(securities)
    return ts, securities

with open(os.path.join(BASE_DIR,'TRADING_SECURITIES.txt'), 'r') as in_f:
    for i,chunk in enumerate(chunks(in_f.readlines(), 100)):
        this_thing = dict()
        for line in chunk:
            ts, securities = parse_trading_securities_line(line)
            this_thing[ts] = securities
        with open(os.path.join(BASE_DIR,'TRADING_SECURITIES_' + str(i) + '.json'), 'w+') as out_f:
            print(i)
            json.dump(this_thing,out_f)

