# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
Table Lookup test set.
"""

import unittest

from tr55.tablelookup import lookup_pet, lookup_bmp_infiltration, lookup_cn


class TestTablelookups(unittest.TestCase):
    """
    Table Lookup test set
    """
    def test_lookup_pet(self):
        """
        Do some spot-checks on the SampleYear data.
        """
        self.assertEqual(lookup_pet(0, 'water')[0], 0.0)
        self.assertEqual(lookup_pet(52, 'hi_residential')[1], 0.0)
        self.assertEqual(lookup_pet(104, 'green_roof')[1], 0.0)
        self.assertEqual(lookup_pet(156, 'cluster_housing')[0], 0.23)
        self.assertEqual(lookup_pet(208, 'grassland')[0], 0.2)
        self.assertEqual(lookup_pet(260, 'woody_wetland')[1], 0.207)
        self.assertEqual(lookup_pet(352, 'hay')[1], 0.207 * 0.6)

    def test_lookup_bmp_infiltration(self):
        """
        Do some spot-checks on the data from Table B.
        """
        self.assertEqual(lookup_bmp_infiltration('d', 'green_roof'), 1.6)
        self.assertEqual(lookup_bmp_infiltration('c', 'porous_paving'), 1.73)
        self.assertEqual(lookup_bmp_infiltration('b', 'rain_garden'), 0.6)
        self.assertEqual(lookup_bmp_infiltration('a', 'infiltration_trench'), 2.4)  # noqa

    def test_lookup_cn(self):
        """
        Do some spot-checks on the data from Table C.
        """
        self.assertEqual(lookup_cn('a', 'water'), 100)
        self.assertEqual(lookup_cn('b', 'li_residential'), 68)
        self.assertEqual(lookup_cn('c', 'hi_residential'), 90)
        self.assertEqual(lookup_cn('d', 'commercial'), 95)
        self.assertEqual(lookup_cn('a', 'rock'), 77)
        self.assertEqual(lookup_cn('b', 'deciduous_forest'), 55)
        self.assertEqual(lookup_cn('c', 'evergreen_forest'), 70)
        self.assertEqual(lookup_cn('d', 'mixed_forest'), 77)

if __name__ == "__main__":
    unittest.main()
