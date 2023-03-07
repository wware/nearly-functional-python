# https://pycon2019.trey.io/iterator-protocol.html

import doctest


def count(n=0):
    """
    >>> c = count()
    >>> next(c)
    start
    0
    >>> next(c)
    loop
    1
    >>> next(c)
    loop
    2
    >>> next(c)
    loop
    3
    """
    print("start")
    while True:
        yield n
        n += 1
        print("loop")
    print("end")



def generatorify(iterable):
    """
    >>> g = generatorify([1, 2, 3, 4])
    >>> g
    <generator object generatorify at 0x...>
    >>> next(g)
    1
    >>> next(g)
    2
    >>> for x in g:
    ...     print(x)
    ...
    3
    4
    """
    for i in iterable:
        yield i


def all_same(it):
    """
    >>> all_same(n % 2 for n in [3, 5, 7, 8])
    False
    >>> all_same(n % 2 for n in [3, 5, 7, 9])
    True
    """
    first = nope = object()
    for i in iter(it):
        if first is nope:
            first = i
        elif first != i:
            return False
    return True


"""
Next I want to do something clever with lazy evaluation and filtering.
Something where the filter lets you avoid some expensive computation.
"""


if __name__ == '__main__':
    doctest.testmod(optionflags=doctest.ELLIPSIS)
