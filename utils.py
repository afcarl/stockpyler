import time
import abc

class FrozenClass(object):
    __isfrozen=False
    def __init__(self):
        self.__isfrozen=False

    def __setattr__(self, key, value):
        if self.__isfrozen:
            raise TypeError( "%r is a frozen class" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed

class NextableClass:

    def __init__(self):
        self._done = False
        self._nextable_children = []

    def add_nextable(self, *nextables):
        self._nextable_children.extend(nextables)

    def all_children_are_done(self):
        return all([c._done for c in self._nextable_children])

    @abc.abstractmethod
    def next(self):
        pass

    def _next(self):
        for n in self._nextable_children:
            n.next()
            n._next()
        if self.all_children_are_done():
            self._done = True

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def _stop(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def _start(self):
        pass
