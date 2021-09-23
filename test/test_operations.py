# -*- coding: utf-8 -*-

"""
Operation tests.
"""

import unittest

from tr55.operations import dict_plus


class TestOperations(unittest.TestCase):
    """
    Dictionary operation test set.
    """
    def test_plus_1(self):
        """
        Test dictionary arithmetic.
        """
        a = {'x': {'y': {'z': {'a': 1, 'b': 3, 'c': 13}, 'n': 144}}}
        b = {'x': {'y': {'z': {'a': 1, 'b': 5, 'c': 21}, 'm': 610}}}
        c = {'x': {'y': {'z': {'a': 2, 'b': 8, 'c': 34}, 'n': 144, 'm': 610}}}
        self.assertEqual(dict_plus(a, b), c)

    def test_plus_2(self):
        """
        Test dictionary arithmetic.
        """
        a = {'x': {'y': {'z': {'a': 2, 'c': 13}, 'n': 144}}}
        b = {'x': {'y': {'z': {'b': 8, 'c': 21}, 'm': 610}}}
        c = {'x': {'y': {'z': {'a': 2, 'b': 8, 'c': 34}, 'n': 144, 'm': 610}}}
        self.assertEqual(dict_plus(a, b), c)

    def test_plus_3(self):
        """
        Test dictionary arithmetic.
        """
        a = {'x': {'y': {'z': {'a': 2, 'c': 13}, 'n': 144}}}
        b = {'x': {'y': None}}
        self.assertEqual(dict_plus(a, b), a)

if __name__ == "__main__":
    unittest.main()
