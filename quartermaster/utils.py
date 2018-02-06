import itertools as it


def find(pred, iterable):
    """
    Find the first occurrence of the predicate function returning true
    over the iterable; otherwise None.
    >>> find(lambda e: e.startswith('g'), ['alpha', 'beta', 'gamma', 'delta'])
    'gamma'
    >>> find(lambda e: e.startswith('p'), ['alpha', 'beta', 'gamma', 'delta'])
    None
    """

    for element in iterable:
        if pred(element):
            return element


def flatten(iter_of_iters, fillvalue=None):
    """
    Flatten one level of nesting. Returns a generator.
    [ [A, B], [C, D], [E, F, G] ] ==> [A, B, C, D, E, F, G]

    in the case of `fillvalue is not None`
    [ [A, B], [], [C, D, E] ] ==> [A, B, X, C, D, E]
        where fillvalue=X
    """

    if fillvalue is None:
        for element in it.chain.from_iterable(iter_of_iters):
            yield element
    else:
        for itr in iter_of_iters:
            if not itr:
                yield fillvalue
            for element in itr:
                yield element


