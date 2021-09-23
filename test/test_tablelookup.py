# -*- coding: utf-8 -*-

"""
Table Lookup test set.
"""

import unittest

from tr55.tablelookup import lookup_bmp_storage, lookup_bmp_drainage_ratio, lookup_cn


class TestTablelookups(unittest.TestCase):
    """
    Table Lookup test set
    """
    def test_lookup_bmp_storage(self):
        """
        Do some spot-checks on the data from Table B.
        """
        self.assertEqual(lookup_bmp_storage('green_roof'), 0.020)
        self.assertEqual(lookup_bmp_storage('infiltration_basin'), 0.610)  # noqa
        self.assertEqual(lookup_bmp_storage('porous_paving'), 0.267)
        self.assertEqual(lookup_bmp_storage('rain_garden'), 0.396)

    def lookup_bmp_drainage(self):
        """
        Do some spot-checks on the data from Table B.
        """
        self.assertEqual(lookup_bmp_drainage_ratio('green_roof'), 1)
        self.assertEqual(lookup_bmp_drainage_ratio('infiltration_basin'), 8)  # noqa
        self.assertEqual(lookup_bmp_drainage_ratio('porous_paving'), 2)
        self.assertEqual(lookup_bmp_drainage_ratio('rain_garden'), 5)

    def test_lookup_cn(self):
        """
        Do some spot-checks on the data from Table C.
        """
        self.assertEqual(lookup_cn('a', 'open_water'), 100)
        self.assertEqual(lookup_cn('b', 'developed_low'), 80)
        self.assertEqual(lookup_cn('c', 'developed_med'), 91)
        self.assertEqual(lookup_cn('d', 'developed_high'), 96)
        self.assertEqual(lookup_cn('a', 'barren_land'), 77)
        self.assertEqual(lookup_cn('b', 'deciduous_forest'), 55)
        self.assertEqual(lookup_cn('c', 'evergreen_forest'), 70)
        self.assertEqual(lookup_cn('d', 'mixed_forest'), 77)

if __name__ == "__main__":
    unittest.main()
