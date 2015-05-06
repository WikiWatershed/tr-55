# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
Operation tests.
"""

import unittest

from tr55.operations import dict_plus, dict_minus


class TestOperations(unittest.TestCase):
    """
    Dictionary operation test set.
    """
    def test_plus(self):
        """
        Test dictionary addition.
        """
        a = {'x': {'y': {'z': {'a': 1, 'b': 3, 'c': 13}}}}
        b = {'x': {'y': {'z': {'a': 1, 'b': 5, 'c': 21}}}}
        c = {'x': {'y': {'z': {'a': 2, 'b': 8, 'c': 34}}}}
        self.assertEqual(dict_plus(a, b), c)

    def test_minus(self):
        """
        Test dictionary subtraction.
        """
        a = {'x': {'y': {'z': {'a': 34, 'b': 144, 'c': 610}}}}
        b = {'x': {'y': {'z': {'a': 21, 'b': 89, 'c': 377}}}}
        c = {'x': {'y': {'z': {'a': 13, 'b': 55, 'c': 233}}}}
        self.assertEqual(dict_minus(a, b), c)

if __name__ == "__main__":
    unittest.main()
