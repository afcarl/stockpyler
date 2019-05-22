def fib(n):
    """Print the Fibonacci series up to n."""
    cdef int a = 0
    cdef int b = 1
    print(a)
    while b < n:
        print(b)
        a, b = b, a + b

    print()