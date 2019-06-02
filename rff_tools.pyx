

cdef struct rff_line:
    cdef long long int timestamp
    cdef char symbol[24]
    cdef double open,high,low,close,volume,turnover,unadj_close,close_ma200,averagefloat,_pad0,_pad1,_pad2

cdef read_rff():
