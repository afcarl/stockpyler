from libc.stdio cimport FILE
from libc.stdint cimport  int64_t
from libcpp cimport bool

import numpy as np

# "cimport" is used to import special compile-time information
# about the numpy module (this is stored in a file numpy.pxd which is
# currently part of the Cython distribution).
cimport numpy as np

cdef extern from "rff_tools.c":

    ctypedef struct rff_line_t:
      np.int64_t timestamp;
      char symbol[24];
      np.float64_t open, high, low, close, volume, turnover, unadj_close, close_ma200, averagefloat, _pad0, _pad1, _pad2;

    ctypedef struct rff_t:
      FILE* file_handle;
      void* mmap_handle;
      rff_line_t* lines;
      np.int64_t len;
      np.int64_t pos;
      bool done;

    cdef int rff_init(char* path, rff_t* rff)
    cdef int rff_close(rff_t* rff)
    cdef rff_line_t* next_rff_line(rff_t* rff)
    cdef rff_line_t* rff_line_at(rff_t* rff, int64_t index)



cdef class RFFLine:
    cdef rff_line_t* _line

    def __init__(self):
        self._line = NULL

    cdef _setup(self, rff_line_t* line):
        self._line = line
        return self
'''
    @property
    def timestamp(self):
       return self._line.timestamp

    @property
    def symbol(self):
        return self._line.symbol.decode('utf-8')
    @property
    def open(self):
        return np.float64(self._line.open)
    @property
    def high(self):
        return self._line.high
    @property
    def low(self):
        return self._line.low
    @property
    def close(self):
        return self._line.close
    @property
    def volume(self):
        return self._line.volume
    @property
    def turnover(self):
        return self._line.turnover
    @property
    def unadj_close(self):
        return self._line.unadj_close
    @property
    def close_ma200(self):
        return self._line.close_ma200
    @property
    def averagefloat(self):
        return self._line.averagefloat
'''

cdef class RFF:
    cdef rff_t rff

    def __init__(self, path):
        ret = rff_init(path.encode('utf-8'), &self.rff)

    def next_line(self):
        line = next_rff_line(&self.rff)
        if line:
            return RFFLine()._setup(line)
        return None

    def get_line(self, index):
        if index >= self.len:
            return None
        line = rff_line_at(&self.rff, index)
        if line:
            return RFFLine()._setup(line)
        return None

    def rewind(self, num_lines):
        self.rff.pos -= num_lines

    @property
    def len(self):
        return self.rff.len
    @property
    def pos(self):
        return self.rff.pos



