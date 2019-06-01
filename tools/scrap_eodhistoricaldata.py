#requires https://github.com/femtotrader/python-eodhistoricaldata
import eod_historical_data
#Exchanges

import requests
import datetime
import pandas as pd
from pandas.io.common import urlencode
from pandas.api.types import is_number
import io
import os

EOD_HISTORICAL_DATA_API_URL = "https://eodhistoricaldata.com/api"

def _init_session(session):
    """
    Returns a requests.Session (or CachedSession)
    """
    if session is None:
        return requests.Session()
    return session


def _url(url, params):
    """
    Returns long url with parameters
    http://mydomain.com?param1=...&param2=...
    """
    if params is not None and len(params) > 0:
        return url + "?" + urlencode(params)
    else:
        return url


class RemoteDataError(IOError):
    """
    Remote data exception
    """
    pass


def _format_date(dt):
    """
    Returns formated date
    """
    if dt is None:
        return dt
    return dt.strftime("%Y-%m-%d")


def _sanitize_dates(start, end):
    """
    Return (datetime_start, datetime_end) tuple
    """
    if is_number(start):
        # regard int as year
        start = datetime.datetime(start, 1, 1)
    start = pd.to_datetime(start)

    if is_number(end):
        # regard int as year
        end = datetime.datetime(end, 1, 1)
    end = pd.to_datetime(end)

    if start is not None and end is not None:
        if start > end:
            raise Exception("end must be after start")

    return start, end

def get_api_key(env_var='EOD_HISTORICAL_API_KEY'):
    """
    Returns API key from environment variable
    API key must have been set previously
    bash> export EOD_HISTORICAL_API_KEY="YOURAPI"
    Returns default API key, if environment variable is not found
    """
    return os.environ.get(env_var, 'EOD_HISTORICAL_API_KEY')

#Exchange Code	Exchange Name
EXCHANGES = [
    'US', #	USA Stocks
    'LSE', #	London Exchange
    'V', #	TSX Venture Exchange
    'TO', #	Toronto Exchange
    'CN', #	Canadian Securities Exchange
    'BE', #	Berlin Exchange
    'HM', #	Hamburg Exchange
    'XETRA', #	XETRA Exchange
    'DU', #	Dusseldorf Exchange
    'HA', #	Hanover Exchange
    'F', #	Frankfurt Exchange
    'MU', #	Munich Exchange
    'STU', #	Stuttgart Exchange
    'LU', #	Luxembourg Stock Exchange
    'VI', #	Vienna Exchange
    'MI', #	Borsa Italiana
    'PA', #	Euronext Paris
    'BR', #	Euronext Brussels
    'SW', #	SIX Swiss Exchange
    'MC', #	Madrid Exchange
    'LS', #	Euronext Lisbon
    'AS', #	Euronext Amsterdam
    'VX', #	Swiss Exchange
    'IR', #	Irish Exchange
    'ST', #	Stockholm Exchange
    'OL', #	Oslo Stock Exchange
    'IC', #	Iceland Exchange
    'CO', #	Coppenhagen Exchange
    'NFN', #	Nasdaq First North
    'NB', #	Nasdaq Baltic
    'HE', #	Helsinki Exchange
    'HK', #	Hong Kong Exchange
    'TA', #	Tel Aviv Exchange
    'KO', #	Korea Stock Exchange
    'KQ', #	KOSDAQ
    'AU', #	Australia Exchange
    'MCX', #	MICEX Russia
    'IS', #	Istanbul Stock Exchange
    'NZ', #	New Zealand Exchange
    'BUD', #	Budapest Stock Exchange
    'WAR', #	Warsaw Stock Exchange
    'PSE', #	Philippine Stock Exchange
    'SG', #	Singapore Exchange
    'BSE', #	Bombay Exchange
    'NSE', #	NSE (India)
    'KAR', #	Karachi Stock Exchange
    'SN', #	Chilean Stock Exchange
    'TSE', #	Tokyo Stock Exchange
    'SR', #	Saudi Arabia Exchange
    'BK', #	Thailand Exchange
    'JSE', #	Johannesburg Exchange
    'SHE', #	Shenzhen Exchange
    'AT', #	Athens Exchange
    'JK', #	Jakarta Exchange
    'SHG', #	Shanghai Exchange
    'VN', #	Vietnam Stocks
    'KLSE', #	Kuala Lumpur Exchange
    'SA', #	Sao Paolo Exchange
    'MX', #	Mexican Exchange
    'IL', #	London IL
    'TW', #	Taiwan Exchange
    'TWO', #	Taiwan OTC Exchange
    'CC', #	Cryptocurrencies
    'INDX', #	Indices
    'COMM', #	Commodities
    'FOREX', #	FOREX
]



def get_bulk_eod(exchange, date, api_key, session=None):
    """
    Returns EOD (end of day data) for a given exchange on given day
    """
    session = _init_session(session)
    endpoint = "/eod-bulk-last-day/{}".format(exchange)
    url = EOD_HISTORICAL_DATA_API_URL + endpoint
    params = {
        "api_token": api_key,
        "date": date
    }
    r = session.get(url, params=params)
    if r.status_code == requests.codes.ok:
        df = pd.read_csv(io.StringIO(r.text), skipfooter=1,
                         parse_dates=[0], index_col=0)
        return df
    else:
        params["api_token"] = "YOUR_HIDDEN_API"
        raise RemoteDataError(r.status_code, r.reason, _url(url, params))

print(get_bulk_eod('US', '2019-01-03', get_api_key()))