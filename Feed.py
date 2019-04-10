import pandas as pd


#Wrapper around a pd.Series
class Feed:
    def __init__(self, data):
        self._data = data
        self._datalen = len(data)
        self._current_position = 0

    def next(self):
        self._current_position += 1

    def __getitem__(self, arg):
        #TODO: what to do about reading before start / after end?
        #have considered negative indicies to return the 0th element, and > len(this) indicies to return the last element
        index = arg + self._current_position
        if index < 0:
            index = 0
        if index > self._datalen:
            index = self._datalen - 1
        return self._data[index]


