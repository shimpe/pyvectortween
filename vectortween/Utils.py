from itertools import tee
from itertools import filterfalse

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def filter_none(list_of_points):
    """
    
    :param list_of_points: 
    :return: 
    """
    return filterfalse(lambda p: p is None or None in p,list_of_points)
