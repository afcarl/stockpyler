import time
import abc
#import tracemalloc
import os
import linecache

class FrozenClass:
    __isfrozen = False

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

class Singleton(type):
    instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
             cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

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
        for n in self._nextable_children:
            n.next()
        if self.all_children_are_done():
            self._done = True

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass


def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))