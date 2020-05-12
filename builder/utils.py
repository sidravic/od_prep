
import itertools

def flatten_list(l):     
    iterable = itertools.chain.from_iterable(l)
    return list(iterable)
