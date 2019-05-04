
import utils
from numba import jitclass
from numba import float32, float64, int32,boolean

spec = [
    ('_data',float32[:]),
    ('_datalen',int32),
    ('_current_position',int32),
    ('_done',boolean),
]

#Wrapper around a pd.Series
class Feed(utils.NextableClass):
    def __init__(self, data):
        super().__init__()

        self._data = data
        self._datalen = len(data) - 1
        self._current_position = 0
        self._done = False

    def next(self):
        self._current_position += 1
        if self._current_position > self._datalen:
            self._done = True

    def __getitem__(self, arg):
        assert arg <= 0, "Can't look into the future!"
        #TODO: what to do about reading before start / after end?
        #have considered negative indicies to return the 0th element, and > len(this) indicies to return the last element
        #TODO: lazy load in/out so we hopefully dont take infinity ram
        index = arg + self._current_position
        if index < 0:
            index = 0
        if index > self._datalen:
            index = self._datalen - 1
        return self._data[index]

#class Indicator(Feed):

#    def __init__(self, df, indicator_func, *args, **kwargs):
#        super().__init__()

