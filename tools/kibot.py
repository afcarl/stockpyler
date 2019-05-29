import io
import os
import urllib.request

import pandas as pd

import common


class KibotApi(metaclass=common.Singleton):

    def __init__(self):
        pass

    def login(self):
        user = os.environ['KIBOT_USER']
        password = os.environ['KIBOT_PASS']
        url = "http://api.kibot.com?action=login&user={}&password={}".format(user,password)
        with urllib.request.urlopen(url) as response:
            html = response.read()

    def request(self, symbol, security_type, interval, interval_type, period, adjusted=True, extended=True):
        url = "http://api.kibot.com/?action=history"
        url += "&symbol=" + symbol
        url += "&type=" + security_type.value
        url += "&period=" + str(period)
        url += "&regularsession=" + "0" if extended else "1"
        url += "&unadjusted=" + "0" if adjusted else "1"

        if interval_type == common.IntervalType.MINUTE:
            url += "&interval=" + str(interval)
        elif interval_type == common.IntervalType.HOUR:
            url += "&interval=" + str(interval * 60)
        elif interval_type == common.IntervalType.DAY:
            url += "&interval=" + interval_type.value
        elif interval_type == common.IntervalType.WEEK:
            url += "&interval=" + interval_type.value

        request = urllib.request.Request(url)
        request.add_header('Accept-encoding', 'gzip')

        with urllib.request.urlopen(url) as response:
            html = response.read()

        if html.decode("utf-8") == '401 Not Logged In':
            self.login()
            with urllib.request.urlopen(url) as response:
                html = response.read()

        return pd.read_csv(io.StringIO(html.decode("utf-8")))


if __name__ == '__main__':
    agent = KibotApi()
    ret = agent.request('qcom', common.SecurityType.STOCK, 1, common.IntervalType.DAY, period=100)
    print(ret)
