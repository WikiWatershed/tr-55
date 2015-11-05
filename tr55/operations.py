# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import sys


def tandem_walk(op, neutral, pred, left, right):
    """
    Walk two similarly-structured dictionaries in tandem, performing
    the given operation when both halves satisfy the given predicate.
    """
    if pred(left) and pred(right):
        return op(left, right)
    elif pred(left) and right is None:
        return op(left, neutral)
    elif left is None and pred(right):
        return op(neutral, right)
    elif isinstance(left, dict) and right is None:
        return left.copy()
    elif left is None and isinstance(right, dict):
        return right.copy()
    elif isinstance(left, dict) and isinstance(right, dict):
        retval = {}
        union = set(left.keys()) | set(right.keys())
        for key in union:
            left_val = left.get(key)
            right_val = right.get(key)
            retval[key] = tandem_walk(op, neutral, pred, left_val, right_val)
        return retval


def is_number(obj):
    """
    Is obj a number?
    """
    if sys.version_info.major == 3:
        types = (int, float)
    else:
        types = (int, long, float)
    return isinstance(obj, types)


def dict_plus(left, right):
    """
    Sum of two similarly-structured dictionaries.
    """
    def plus(x, y):
        return x + y
    return tandem_walk(plus, 0, is_number, left, right)
