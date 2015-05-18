# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
Operation tests.
"""

import unittest

from tr55.operations import dict_plus


class TestOperations(unittest.TestCase):
    """
    Dictionary operation test set.
    """
    def test_plus(self):
        """
        Test dictionary addition.
        """
        a = {'x': {'y': {'z': {'a': 1, 'b': 3, 'c': 13}, 'n': 144}}}
        b = {'x': {'y': {'z': {'a': 1, 'b': 5, 'c': 21}, 'm': 610}}}
        c = {'x': {'y': {'z': {'a': 2, 'b': 8, 'c': 34}, 'n': 144, 'm': 610}}}
        self.assertEqual(dict_plus(a, b), c)

if __name__ == "__main__":
    unittest.main()
