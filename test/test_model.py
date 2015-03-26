"""
Model test set
"""

import unittest
from tr55.model import *

# These data are taken directly from Table 2-1 of the revised (1986)
# TR-55 report.  The Ps array are various precipitation levels, and
# the CNx array is the calculated runoff for that particular curve
# number with the given level of precipitation.
Ps = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
CN55 = [0.000, 0.000, 0.000, 0.000, 0.000, 0.020, 0.080, 0.190, 0.350, 0.530, 0.740, 0.980, 1.520, 2.120, 2.780, 3.490, 4.230, 5.000, 5.790, 6.610, 7.440, 8.290]
CN70 = [0.000, 0.030, 0.060, 0.110, 0.170, 0.240, 0.460, 0.710, 1.010, 1.330, 1.670, 2.040, 2.810, 3.620, 4.460, 5.330, 6.220, 7.130, 8.050, 8.980, 9.910, 10.85]
CN80 = [0.080, 0.150, 0.240, 0.340, 0.440, 0.560, 0.890, 1.250, 1.640, 2.040, 2.460, 2.890, 3.780, 4.690, 5.630, 6.570, 7.520, 8.480, 9.450, 10.42, 11.39, 12.37]
CN90 = [0.320, 0.460, 0.610, 0.760, 0.930, 1.090, 1.530, 1.980, 2.450, 2.920, 3.400, 3.880, 4.850, 5.820, 6.810, 7.790, 8.780, 9.770, 10.76, 11.76, 12.75, 13.74]

class TestModel(unittest.TestCase):
    """
    Model test set
    """
    def test_NRCS(self):
        """
        Test the implementation of the runoff equation.
        """
        # This pair has CN=55 in Table C of the 2010/12/27 memo
        Qs = [round(runoffNRCS(P, 'soilB', 'DeciduousForest'), 2) for P in Ps]
        self.assertEqual(Qs[3:], CN55[3:]) # Low curve number and low P cause too-high runoff

        # This pair has CN=70
        Qs = [round(runoffNRCS(P, 'soilC', 'DeciduousForest'), 2) for P in Ps]
        self.assertEqual(Qs, CN70)

        # This pair has CN=80
        Qs = [round(runoffNRCS(P, 'soilD', 'Pasture'), 2) for P in Ps]
        self.assertEqual(Qs, CN80)

        # This pair has CN=90
        Qs = [round(runoffNRCS(P, 'soilC', 'HI_Residential'), 2) for P in Ps]
        self.assertEqual(Qs, CN90)

    def test_tileByTileTR55(self):
        """
        Test the tile-by-tile simulation.
        """
        # Test invalid responses
        nonResponse = {
            "error": {
                "message": "boom!",
                "trace": "blah at line 2"
            }
        }
        self.assertRaises(Exception, tileByTileTR55, (date.today(), nonResponse))

        # Test valid responses
        response1 = {
            "result": {
                "cell_count": 2,
                "distribution": {
                    "soilA:Pasture": 1,
                    "soilC:Rock": 1
                }
            }
        }
        response2 = {
            "result": {
                "cell_count": 20,
                "distribution": {
                    "soilA:Pasture": 10,
                    "soilC:Rock": 10
                }
            }
        }
        self.assertEqual(tileByTileTR55(date.today(), response1),
                         tileByTileTR55(date.today(), response2))

        response3 = {
            "result": {
                "cell_count": 1,
                "distribution": {
                    "soilD:HI_Residential": 1
                }
            }
        }
        response4 = {
            "result": {
                "cell_count": 10,
                "distribution": {
                    "soilD:Pasture": 10
                }
            }
        }
        self.assertEqual(tileByTileTR55(date.today(), response3, True),
                         tileByTileTR55(date.today(), response4, True))

if __name__ == "__main__":
    unittest.main()
