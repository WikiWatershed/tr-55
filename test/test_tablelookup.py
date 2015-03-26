"""
Table Lookup test set
"""

import unittest
from datetime import date
from tr55.tables import *
from tr55.tablelookup import *

class TestTablelookups(unittest.TestCase):
    """
    Table Lookup test set
    """
    def test_consistency_and_typos(self):
        """
        Test for consistency of key names in the various tables.
        """
        # Make sure that the same BMP names are used in Table B
        self.assertEqual(TableB['soilA'].keys(), TableB['soilB'].keys())
        self.assertEqual(TableB['soilB'].keys(), TableB['soilC'].keys())
        self.assertTrue(TableB['soilD'].keys()[0] in TableB['soilA'].keys())

        # Make sure that the same names are used in Table C
        self.assertEqual(TableC['soilA'].keys(), TableC['soilB'].keys())
        self.assertEqual(TableC['soilB'].keys(), TableC['soilC'].keys())
        self.assertEqual(TableC['soilC'].keys(), TableC['soilD'].keys())

        # Make sure that the same names are used everywhere
        self.assertEqual(set(TableA.keys()), set(TableC['soilA'].keys() + TableB['soilA'].keys()))

    def test_lookupP(self):
        """
        Do some spot-checks on the SampleYear data.
        """
        self.assertEqual(lookupP(date(1, 10, 15)), 0.0)
        self.assertEqual(lookupP(date(1, 2, 12)), 0.01)
        self.assertEqual(lookupP(date(1, 2, 15)), 0.01)
        self.assertEqual(lookupP(date(1, 2, 19)), 0.02)
        self.assertEqual(lookupP(date(1, 10, 14)), 0.0)

    def test_lookupET(self):
        """
        Do some spot-checks on Table A.
        """
        self.assertEqual(lookupET(date(1, 4, 15), 'WoodyWetland'), 0.207)
        self.assertEqual(lookupET(date(1, 10, 14), 'WoodyWetland'), 0.207)
        self.assertTrue(lookupET(date(1, 6, 15), 'Commercial') > 0.0)
        self.assertEqual(lookupET(date(1, 4, 14), 'WoodyWetland'), 0.0)
        self.assertEqual(lookupET(date(1, 10, 15), 'WoodyWetland'), 0.0)

    def test_lookupBMPInfiltration(self):
        """
        Do some spot-checks on Table B.
        """
        self.assertEqual(lookupBMPInfiltration('soilD', 'GreenRoof'), 1.6)
        self.assertEqual(lookupBMPInfiltration('soilC', 'PorousPaving'), 1.73)
        self.assertEqual(lookupBMPInfiltration('soilB', 'RainGarden'), 0.6)
        self.assertEqual(lookupBMPInfiltration('soilA', 'InfiltrationTrench'), 2.4)

    def test_lookupCN(self):
        """
        Do some spot-checks on Table C.
        """
        self.assertEqual(lookupCN('soilA', 'Water'), 100)
        self.assertEqual(lookupCN('soilB', 'LI_Residential'), 68)
        self.assertEqual(lookupCN('soilC', 'HI_Residential'), 90)
        self.assertEqual(lookupCN('soilD', 'Commercial'), 95)
        self.assertEqual(lookupCN('soilA', 'Rock'), 77)
        self.assertEqual(lookupCN('soilB', 'DeciduousForest'), 55)
        self.assertEqual(lookupCN('soilC', 'EvergreenForest'), 70)
        self.assertEqual(lookupCN('soilD', 'MixedForest'), 77)

if __name__ == "__main__":
    unittest.main()
