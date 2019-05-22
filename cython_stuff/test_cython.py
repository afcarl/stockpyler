import pyximport
pyximport.install(language_level=3)

import cython_stuff.fib

def test_simple():
    cython_stuff.fib.fib(20)
    pass
    #fib(10)

