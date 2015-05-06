# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import sys


def tandem_walk(op, pred, left, right):
    """
    Walk two similarly-structured dictionaries in tandem, performing
    the given operation when both halves satisfy the given predicate.
    Otherwise, if both haves are dictionaries, recurse.
    """
    if pred(left) and pred(right):
        return op(left, right)
    elif isinstance(left, dict) and isinstance(right, dict):
        retval = left.copy()
        left_set = set(left.keys())
        right_set = set(right.keys())
        intersection = left_set & right_set
        difference = right_set - left_set
        for key in intersection:
            retval[key] = tandem_walk(op, pred, left[key], right[key])
        for key in difference:
            retval[key] = right[key]
        return retval


def isnumber(obj):
    """
    Is obj a number?
    """
    if sys.version_info.major == 3:
        types = (int, float)
    else:
        types = (int, long, float)
    return isinstance(obj, types)


def plus(x, y):
    """
    Sum of two numbers.
    """
    return x + y


def dict_plus(left, right):
    """
    Sum of two similarly-structured dictionaries.
    """
    return tandem_walk(plus, isnumber, left, right)
