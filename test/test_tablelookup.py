"""
Table Lookup test set
"""

import unittest
from datetime import date
from tr55.tables import TABLE_A, TABLE_B, TABLE_C
from tr55.tablelookup import lookup_et, lookup_p, lookup_bmp_infiltration, lookup_cn


class TestTablelookups(unittest.TestCase):
    """
    Table Lookup test set
    """
    def test_consistency_and_typos(self):
        """
        Test for consistency of key names in the various tables.
        """
        # Make sure that the same BMP names are used in Table B
        self.assertEqual(TABLE_B['soilA'].keys(), TABLE_B['soilB'].keys())
        self.assertEqual(TABLE_B['soilB'].keys(), TABLE_B['soilC'].keys())
        self.assertTrue(TABLE_B['soilD'].keys()[0] in TABLE_B['soilA'].keys())

        # Make sure that the same names are used in Table C
        self.assertEqual(TABLE_C['soilA'].keys(), TABLE_C['soilB'].keys())
        self.assertEqual(TABLE_C['soilB'].keys(), TABLE_C['soilC'].keys())
        self.assertEqual(TABLE_C['soilC'].keys(), TABLE_C['soilD'].keys())

        # Make sure that the same names are used everywhere
        self.assertEqual(set(TABLE_A.keys()), set(TABLE_C['soilA'].keys() + TABLE_B['soilA'].keys()))

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
        Do some spot-checks on Table A.
        """
        self.assertEqual(lookup_et(date(1, 4, 15), 'WoodyWetland'), 0.207)
        self.assertEqual(lookup_et(date(1, 10, 14), 'WoodyWetland'), 0.207)
        self.assertTrue(lookup_et(date(1, 6, 15), 'Commercial') > 0.0)
        self.assertEqual(lookup_et(date(1, 4, 14), 'WoodyWetland'), 0.0)
        self.assertEqual(lookup_et(date(1, 10, 15), 'WoodyWetland'), 0.0)

    def test_lookup_bmp_infiltration(self):
        """
        Do some spot-checks on Table B.
        """
        self.assertEqual(lookup_bmp_infiltration('soilD', 'GreenRoof'), 1.6)
        self.assertEqual(lookup_bmp_infiltration('soilC', 'PorousPaving'), 1.73)
        self.assertEqual(lookup_bmp_infiltration('soilB', 'RainGarden'), 0.6)
        self.assertEqual(lookup_bmp_infiltration('soilA', 'InfiltrationTrench'), 2.4)

    def test_lookup_cn(self):
        """
        Do some spot-checks on Table C.
        """
        self.assertEqual(lookup_cn('soilA', 'Water'), 100)
        self.assertEqual(lookup_cn('soilB', 'LI_Residential'), 68)
        self.assertEqual(lookup_cn('soilC', 'HI_Residential'), 90)
        self.assertEqual(lookup_cn('soilD', 'Commercial'), 95)
        self.assertEqual(lookup_cn('soilA', 'Rock'), 77)
        self.assertEqual(lookup_cn('soilB', 'DeciduousForest'), 55)
        self.assertEqual(lookup_cn('soilC', 'EvergreenForest'), 70)
        self.assertEqual(lookup_cn('soilD', 'MixedForest'), 77)

if __name__ == "__main__":
    unittest.main()
