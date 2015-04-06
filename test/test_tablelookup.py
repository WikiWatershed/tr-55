"""
Table Lookup test set
"""

import unittest
from datetime import date
from tr55.tables import LAND_USE_VALUES
from tr55.tablelookup import lookup_et, lookup_p, lookup_bmp_infiltration, lookup_cn


class TestTablelookups(unittest.TestCase):
    """
    Table Lookup test set
    """
    def test_lookup_p(self):
        """
        Do some spot-checks on the SampleYear data.
        """
        self.assertEqual(lookup_p(date(1, 10, 15)), 0.0)
        self.assertEqual(lookup_p(date(1, 2, 12)), 0.01)
        self.assertEqual(lookup_p(date(1, 2, 15)), 0.01)
        self.assertEqual(lookup_p(date(1, 2, 19)), 0.02)
        self.assertEqual(lookup_p(date(1, 10, 14)), 0.0)

    def test_lookup_et(self):
        """
        Do some spot-checks on the data from Table A.
        """
        self.assertEqual(lookup_et(date(1, 4, 15), 'woody_wetland'), 0.207)
        self.assertEqual(lookup_et(date(1, 10, 14), 'woody_wetland'), 0.207)
        self.assertTrue(lookup_et(date(1, 6, 15), 'commercial') > 0.0)
        self.assertEqual(lookup_et(date(1, 4, 14), 'woody_wetland'), 0.0)
        self.assertEqual(lookup_et(date(1, 10, 15), 'woody_wetland'), 0.0)

    def test_lookup_bmp_infiltration(self):
        """
        Do some spot-checks on the data from Table B.
        """
        self.assertEqual(lookup_bmp_infiltration('d', 'green_roof'), 1.6)
        self.assertEqual(lookup_bmp_infiltration('c', 'porous_paving'), 1.73)
        self.assertEqual(lookup_bmp_infiltration('b', 'rain_garden'), 0.6)
        self.assertEqual(lookup_bmp_infiltration('a', 'infiltration_trench'), 2.4)

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
