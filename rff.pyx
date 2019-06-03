from libc.stdio cimport FILE
from libc.stdint cimport  int64_t
from libcpp cimport bool

cdef extern from "rff_tools.c":

    ctypedef struct rff_line_t:
      long long int timestamp;
      char symbol[24];
      double open, high, low, close, volume, turnover, unadj_close, close_ma200, averagefloat, _pad0, _pad1, _pad2;

    ctypedef struct rff_t:
      FILE* file_handle;
      void* mmap_handle;
      rff_line_t* lines;
      int64_t len;
      int64_t pos;
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

    @property
    def timestamp(self):
       return self._line.timestamp

    @property
    def symbol(self):
        return self._line.symbol.decode('utf-8')
    @property
    def open(self):
        return self._line.open
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

cdef class RFF:
    cdef rff_t rff

    def __init__(self, path):
        ret = rff_init(path.encode('utf-8'), &self.rff)

    def next_line(self):
        r = next_rff_line(&self.rff)
        return get_line(r)

    def get_line(self, index):
        if index >= self.len:
            return None
        r = rff_line_at(&self.rff, index)
        return get_line(r)

    @property
    def len(self):
        return self.rff.len
    @property
    def pos(self):
        return self.rff.pos





cdef get_line(rff_line_t* line):
    if line:
        return RFFLine()._setup(line)
    return None

def py_rff_init(str path):
    return RFF(path)

cdef py_rff_close(rff_t* rff):
    ret = rff_close(rff)
    return ret

cdef py_rff_readline(rff_t* rff):
    r = next_rff_line(rff)
    return get_line(r)
    #pyobj._setup(r)
    #return pyobj
