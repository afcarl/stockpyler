import utils


class SimpleMovingAverage(utils.NextableClass):

    def __init__(self, history, member, period, *args, **kwargs):
        super().__init__()
        self._history = history
        self._member = member
        self._period = period
        self._cursize = 0
        self._cursum = 0
        self._pos = -1
        self.rows = []

    def start(self):
        self.next()

    def next(self):
        a = sum([t[self._member] for t in self._history[-self._period:]]) / self._period
        self.rows.append(a)
        if len(self.rows) > self._period * 4:
            self.rows = self.rows[-self._period*2]
            self._pos -= self._period*2

        self._pos += 1

        #sma = sum([self._member])
        #self.rows.append()