import pandas as pd
import abc
import utils

#Wrapper around a pd.Series
class Feed(utils.NextableClass):
    def __init__(self, data):
        super().__init__()
        self._data = data.tolist()
        self._datalen = len(data) - 1
        self._current_position = 0
        self._done = False

    @abc.abstractmethod
    def next(self):
        pass

    def _next(self):
        self._current_position += 1
        if self._current_position > self._datalen:
            self._done = True


    def __getitem__(self, arg):
        #TODO: what to do about reading before start / after end?
        #have considered negative indicies to return the 0th element, and > len(this) indicies to return the last element
        index = arg + self._current_position
        if index < 0:
            index = 0
        if index > self._datalen:
            index = self._datalen - 1
        return self._data[index]


