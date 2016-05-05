# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
Model test set
"""

import unittest

from tr55.model import runoff_nrcs, runoff_pitt, \
    simulate_cell_day, simulate_water_quality, \
    create_unmodified_census, create_modified_census, \
    simulate_day, compute_bmp_effect
from tr55.tablelookup import lookup_ki

# These data are taken directly from Table 2-1 of the revised (1986)
# TR-55 report.  The data in the PS array are various precipitation
# levels, and each respective CNx array is the calculated runoff for
# that particular curve number with the given level of precipitation
# corresponding to that in PS.
PS = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]  # noqa
CN55 = [0.000, 0.000, 0.000, 0.000, 0.000, 0.020, 0.080, 0.190, 0.350, 0.530, 0.740, 0.980, 1.520, 2.120, 2.780, 3.490, 4.230, 5.000, 5.790, 6.610, 7.440, 8.290]  # noqa
CN70 = [0.000, 0.030, 0.060, 0.110, 0.170, 0.240, 0.460, 0.710, 1.010, 1.330, 1.670, 2.040, 2.810, 3.620, 4.460, 5.330, 6.220, 7.130, 8.050, 8.980, 9.910, 10.85]  # noqa
CN80 = [0.080, 0.150, 0.240, 0.340, 0.440, 0.560, 0.890, 1.250, 1.640, 2.040, 2.460, 2.890, 3.780, 4.690, 5.630, 6.570, 7.520, 8.480, 9.450, 10.42, 11.39, 12.37]  # noqa
CN90 = [0.320, 0.460, 0.610, 0.760, 0.930, 1.090, 1.530, 1.980, 2.450, 2.920, 3.400, 3.880, 4.850, 5.820, 6.810, 7.790, 8.780, 9.770, 10.76, 11.76, 12.75, 13.74]  # noqa
CN95 = [0.560, 0.740, 0.920, 1.110, 1.290, 1.480, 1.960, 2.450, 2.940, 3.430, 3.920, 4.420, 5.410, 6.410, 7.400, 8.400, 9.400, 10.39, 11.39, 12.39, 13.39, 14.39]  # noqa
# These are runoffs calculated by Sara Damiano.
PS_PITT = [0.01, 0.08, 0.12, 0.2, 0.39, 0.59, 0.79, 0.98, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.5, 3.9, 4.9]
PITT_RES_A = [0.0008,0.0089,0.0172,0.0320,0.0718,0.1211,0.1689,0.2143,0.2699,0.3685,0.4717,0.5718,0.6753,0.7806,0.8626,0.9692,1.2363]
PITT_COMM_C = [0.0020,0.0225,0.0484,0.0979,0.2265,0.3751,0.5275,0.6728,0.8508,1.1836,1.5448,1.8767,2.2189,2.5615,2.8206,3.1969,4.1109]
PITT_OPEN_B = [0.0004,0.0038,0.0072,0.0129,0.0459,0.0862,0.1293,0.1663,0.2171,0.2998,0.6254,0.7554,0.8862,1.0182,1.1196,1.2502,1.5824]

# A census containing several land covers and several land cover modifications.
# This includes BMP's that act as land cover changes.
CENSUS_1 = {
    'cell_count': 147,
    'distribution': {
        'c:developed_high': {
            'cell_count': 42
        },
        'a:deciduous_forest': {
            'cell_count': 72
        },
        'd:developed_med': {
            'cell_count': 33
        }
    },
    'modifications': [
        {
            'change': '::no_till',
            'cell_count': 30,
            'distribution': {
                'c:developed_high': {
                    'cell_count': 20
                },
                'd:developed_med': {
                    'cell_count': 10
                }
            }
        },
        {
            'change': 'd:barren_land:',
            'cell_count': 5,
            'distribution': {
                'a:deciduous_forest': {
                    'cell_count': 5
                }
            },
        }
    ]
}

DAY_OUTPUT_1 = {
    "unmodified": {
        "cell_count": 147,
        "distribution": {
            "c:developed_high": {
                "cell_count": 42,
                "et": 0.01242,
                "inf": 0.4427799999999999,
                "runoff": 1.5447999999999997,
                "tn": 0.3306779631791999,
                "tp": 0.05232706230527999,
                "bod": 45.05941476287999,
                "tss": 9.1899403173648
            },
            "a:deciduous_forest": {
                "bod": 0.0,
                "cell_count": 72,
                "et": 0.207,
                "inf": 1.7930000000000001,  # should be 0.03726, but float point rounding issues
                "runoff": 0.0,
                "tn": 0.0,
                "tp": 0.0,
                "tss": 0.0
            },
            "d:developed_med": {
                "cell_count": 33,
                "et": 0.037259999999999995,  # should be 0.03726, but float point rounding issues
                "inf": 0.6482460872656175,
                "runoff": 1.3144939127343824,
                "tn": 0.16641995531964812,
                "tp": 0.027939116586510267,
                "bod": 28.667963106158364,
                "tss": 3.425578642346042
            }
        },
        "et": 0.1133008163265306,
        "inf": 1.1502372848963631,
        "runoff": 0.7364618987771062,
        "tn": 0.497097918498848,
        "tp": 0.08026617889179026,
        "bod": 73.72737786903835,
        "tss": 12.61551895971084
    },
    "modified": {
        "cell_count": 147,
        "distribution": {
            "a:deciduous_forest": {
                'inf': 1.7060957171334694,
                'cell_count': 72,
                'tp': 3.9101893977641545e-05,
                'tn': 0.0003910189397764155,
                'runoff': 0.09696678286653043,
                'et': 0.1969375,
                'distribution': {
                    'a:deciduous_forest': {
                        'cell_count': 67,
                        'tp': 0.0,
                        'tn': 0.0,
                        'runoff': 0.0,
                        'et': 0.207,
                        'inf': 1.793,
                        'bod': 0.0,
                        'tss': 0.0
                    },
                    'd:barren_land:': {
                        'cell_count': 5,
                        'tp': 3.9101893977641545e-05,
                        'tn': 0.0003910189397764155,
                        'runoff': 1.3963216732780384,
                        'et': 0.0621,
                        'inf': 0.5415783267219616,
                        'bod': 5.1614500050486845,
                        'tss': 0.03910189397764155
                    }
                },
                'bod': 5.1614500050486845,
                'tss': 0.03910189397764155
            },
            "c:developed_high": {
                'inf': 0.7866861254657073,
                'cell_count': 42,
                'tp': 0.03787323138005428,
                'tn': 0.23933778163784303,
                'runoff': 1.1180938745342925,
                'et': 0.09522,
                'distribution': {
                    'c:developed_high:no_till': {
                        'cell_count': 20,
                        'tp': 0.010463817791574277,
                        'tn': 0.06612551521064301,
                        'runoff': 0.6487171365220146,
                        'et': 0.1863,
                        'inf': 1.1649828634779853,
                        'bod': 9.010509764966741,
                        'tss': 1.8377079996452328
                    },
                    'c:developed_high': {
                        'cell_count': 22,
                        'tp': 0.02740941358848,
                        'tn': 0.1732122664272,
                        'runoff': 1.5448,
                        'et': 0.012419999999999999,
                        'inf': 0.44277999999999995,
                        'bod': 23.60255059008,
                        'tss': 4.813778261476799
                    }
                },
                'bod': 32.61306035504674,
                'tss': 6.651486261122033
            },
            "d:developed_med": {
                'inf': 0.7441409145669375,
                'cell_count': 33,
                'tp': 0.024940967394893893,
                'tn': 0.14856141448262886,
                'runoff': 1.173435449069426,
                'et': 0.08242363636363635,
                'distribution': {
                    'd:developed_med:no_till': {
                        'cell_count': 10,
                        'tp': 0.005468249773992795,
                        'tn': 0.03257174865378317,
                        'runoff': 0.8490009826400262,
                        'et': 0.1863,
                        'inf': 0.9646990173599737,
                        'bod': 5.610899768096954,
                        'tss': 0.6704549722895514
                    },
                    'd:developed_med': {
                        'cell_count': 23,
                        'tp': 0.0194727176209011,
                        'tn': 0.11598966582884568,
                        'runoff': 1.3144939127343824,
                        'et': 0.037259999999999995,
                        'inf': 0.6482460872656175,
                        'bod': 19.980701558837648,
                        'tss': 2.387524508301787
                    }
                },
                'bod': 25.5916013269346,
                'tss': 3.0579794805913383
            }
        },
        "et": 0.1421681632653061,
        "inf": 1.2274582250603976,
        "runoff": 0.6303736116742962,
        "tn": 0.3882902150602483,
        "tp": 0.06285330066892582,
        "bod": 63.36611168703003,
        "tss": 9.748567635691012
    }
}

CENSUS_2 = {
    'cell_count': 40,
    'BMPs': {
        'rain_garden': 8,
        'green_roof': 16
    },
    'distribution': {
        'd:developed_med': {'cell_count': 10},
        'c:developed_high': {'cell_count': 10},
        'a:deciduous_forest': {'cell_count': 10},
        'b:pasture': {'cell_count': 10}
    },
    'modifications': [
        {
            'change': '::no_till',
            'cell_count': 1,
            'distribution': {
                'b:pasture': {'cell_count': 1}
            }
        },
        {
            'change': '::cluster_housing',
            'cell_count': 1,
            'distribution': {
                'd:developed_med': {'cell_count': 1}
            }
        }
    ]
}

DAY_OUTPUT_2 = {
    'unmodified': {
        'BMPs': {
            'rain_garden': 8,
            'green_roof': 16
        },
        'inf': 1.1535619337299798,
        'cell_count': 40,
        'tp': 0.02215393321295682,
        'tn': 0.1385832470154011,
        'et': 0.11333250000000002,
        'runoff': 0.7331055662700201,
        'distribution': {
            'a:deciduous_forest': {
                'cell_count': 10,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 0.207,
                'inf': 1.793,
                'bod': 0.0,
                'tss': 0.0
            },
            'b:pasture': {
                'cell_count': 10,
                'tp': 0.0012287098889476472,
                'tn': 0.00942010914859863,
                'runoff': 0.0731283523456977,
                'et': 0.19665,
                'inf': 1.7302216476543024,
                'bod': 0.40956996298254905,
                'tss': 0.20478498149127453
            },
            'c:developed_high': {
                'cell_count': 10,
                'tp': 0.012458824358399997,
                'tn': 0.07873284837599999,
                'runoff': 1.5448,
                'et': 0.012419999999999999,
                'inf': 0.44277999999999995,
                'bod': 10.728432086399998,
                'tss': 2.1880810279439995
            },
            'd:developed_med': {
                'cell_count': 10,
                'tp': 0.008466398965609172,
                'tn': 0.050430289490802464,
                'runoff': 1.3144939127343824,
                'et': 0.037259999999999995,
                'inf': 0.6482460872656175,
                'bod': 8.687261547320718,
                'tss': 1.0380541340442553
            }
        },
        'bod': 19.825263596703266,
        'tss': 3.430920143479529
    },
    'modified': {
        'BMPs': {
            'rain_garden': 8,
            'green_roof': 16
        },
        'inf': 1.3866270217345416,
        'cell_count': 40,
        'tp': 0.015263868963184515,
        'tn': 0.09592894322633824,
        'et': 0.11431574999999998,
        'runoff': 0.4990572282654582,
        'bod': 13.479967443369933,
        'tss': 2.372178823187574,
        'distribution': {
            'a:deciduous_forest': {
                'inf': 1.793,
                'cell_count': 10,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 0.207,
                'bod': 0.0,
                'tss': 0.0,
                'distribution': {
                    'a:deciduous_forest': {
                        'cell_count': 10,
                        'tp': 0.0,
                        'tn': 0.0,
                        'runoff': 0.0,
                        'et': 0.207,
                        'inf': 1.793,
                        'bod': 0.0,
                        'tss': 0.0
                    }
                }
            },
            'b:pasture': {
                'inf': 1.7375451880661668,
                'cell_count': 10,
                'tp': 0.0011230492040934608,
                'tn': 0.008610043898049865,
                'runoff': 0.06683981193383332,
                'et': 0.19561499999999998,
                'bod': 0.3743497346978202,
                'tss': 0.1871748673489101,
                'distribution': {
                    'b:pasture:no_till': {
                        'cell_count': 1,
                        'tp': 0.0003676260159800975,
                        'tn': 0.002818466122514081,
                        'runoff': 0.2187976598044872,
                        'et': 0.1863,
                        'inf': 1.594902340195513,
                        'bod': 0.12254200532669915,
                        'tss': 0.061271002663349575
                    },
                    'b:pasture': {
                        'cell_count': 9,
                        'tp': 0.0007554231881133633,
                        'tn': 0.005791577775535785,
                        'runoff': 0.04995560661487177,
                        'et': 0.19665,
                        'inf': 1.7533943933851281,
                        'bod': 0.25180772937112106,
                        'tss': 0.12590386468556053
                    }
                }
            },
            'c:developed_high': {
                'inf': 0.9322927054928913,
                'cell_count': 10,
                'tp': 0.00851090047249819,
                'tn': 0.05378416270814828,
                'runoff': 1.0552872945071088,
                'et': 0.012419999999999999,
                'bod': 7.328830962428997,
                'tss': 1.4947268954824948,
                'distribution': {
                    'c:developed_high': {
                        'cell_count': 10,
                        'tp': 0.00851090047249819,
                        'tn': 0.05378416270814828,
                        'runoff': 1.0552872945071088,
                        'et': 0.012419999999999999,
                        'inf': 0.9322927054928913,
                        'bod': 7.328830962428997,
                        'tss': 1.4947268954824948
                    }
                }
            },
            'd:developed_med': {
                'inf': 1.0836701933791093,
                'cell_count': 10,
                'tp': 0.0056299192865928655,
                'tn': 0.03353473662014011,
                'runoff': 0.8741018066208908,
                'et': 0.042228,
                'bod': 5.776786746243115,
                'tss': 0.6902770603561688,
                'distribution': {
                    'd:developed_med': {
                        'cell_count': 9,
                        'tp': 0.005205227170359879,
                        'tn': 0.031005048797361014,
                        'runoff': 0.8979600756185461,
                        'et': 0.037259999999999995,
                        'inf': 1.0647799243814537,
                        'bod': 5.341015705238832,
                        'tss': 0.6382061139310807
                    },
                    'd:developed_med:cluster_housing': {
                        'cell_count': 1,
                        'tp': 0.00042469211623298705,
                        'tn': 0.002529687822779097,
                        'runoff': 0.6593773856419921,
                        'et': 0.08693999999999999,
                        'inf': 1.253682614358008,
                        'bod': 0.4357710410042824,
                        'tss': 0.052070946425087986
                    }
                }
            }
        }
    }
}


def simulate(precip, tile_string):
    land_use = tile_string.split(':')[1]
    ki = lookup_ki(land_use)
    return simulate_cell_day(precip, 0.207 * ki, tile_string, 1)


def average(l):
    return reduce(lambda x, y: x + y, l) / len(l)


class TestModel(unittest.TestCase):
    """
    Model test set.
    """
    def test_nrcs(self):
        """
        Test the implementation of the runoff equation.
        """
        # This pair has CN=55
        runoffs = [round(runoff_nrcs(precip, 0.0, 'b', 'deciduous_forest'), 2)
                   for precip in PS]
        # Low curve number and low P cause too-high runoff
        self.assertEqual(runoffs[4:], CN55[4:])

        # This pair has CN=70
        runoffs = [round(runoff_nrcs(precip, 0.0, 'c', 'deciduous_forest'), 2)
                   for precip in PS]
        self.assertEqual(runoffs[1:], CN70[1:])

        # This pair has CN=80
        runoffs = [round(runoff_nrcs(precip, 0.0, 'd', 'pasture'), 2)
                   for precip in PS]
        self.assertEqual(runoffs, CN80)

        # This pair has CN=90 - SRGD Updated curve numbers on 2/25/16 - this is no longer true
        # runoffs = [round(runoff_nrcs(precip, 0.0, 'c', 'developed_med'), 2)
        #            for precip in PS]
        # self.assertEqual(runoffs, CN90)

        # This pair has CN=95
        runoffs = [round(runoff_nrcs(precip, 0.0, 'c', 'developed_high'), 2)
                   for precip in PS]
        self.assertEqual(runoffs, CN95)

    def test_pitt(self):
        """
        Test the implementation of the SSH/Pitt runoff model.
        """
        runoff_modeled = [round(runoff_pitt(precip, 0.0, 'c', 'developed_high'), 2)
                   for precip in PS_PITT]
        runnoff_test_suite = [round(runoff,2)
                   for runoff in PITT_COMM_C]
        self.assertEqual(runnoff_test_suite, runoff_modeled)
        runoff_modeled = [round(runoff_pitt(precip, 0.0, 'b', 'developed_open'), 2)
                   for precip in PS_PITT]
        runnoff_test_suite = [round(runoff,2)
                   for runoff in PITT_OPEN_B]
        self.assertEqual(runoff_modeled, runnoff_test_suite)
        runoff_modeled = [round(runoff_pitt(precip, 0.0, 'a', 'developed_low'), 2)
                   for precip in PS_PITT]
        runnoff_test_suite = [round(runoff,2)
                   for runoff in PITT_RES_A]
        self.assertEqual(runoff_modeled, runnoff_test_suite)

    def test_simulate_cell_day(self):
        """
        Test the simulate_cell_day function.
        """
        result1 = simulate_cell_day(42, 93, 'a:barren_land:', 1)
        result2 = simulate_cell_day(42, 93, 'a:barren_land:', 2)
        self.assertEqual(result1['runoff-vol'] * 2, result2['runoff-vol'])

    def test_create_unmodified_census(self):
        """
        Test create_unmodified_census.
        """
        census = {
            "cell_count": 2,
            "distribution": {
                "a:barren_land": {"cell_count": 1},
                "a:open_water": {"cell_count": 1}
            },
            "modifications": [
                {
                    "change": "::cluster_housing",
                    "cell_count": 1,
                    "distribution": {
                        "a:barren_land": {"cell_count": 1}
                    }
                }
            ]
        }

        result = create_unmodified_census(census)
        census.pop("modifications", None)
        self.assertEqual(census, result)

    def test_create_modified_census_1(self):
        """
        create_modified_census from a census w/o modifications.
        """
        census = {
            "cell_count": 5,
            "distribution": {
                "a:barren_land": {"cell_count": 3},
                "a:open_water": {"cell_count": 2}
            }
        }

        expected = {
            "cell_count": 5,
            "distribution": {
                "a:barren_land": {
                    "cell_count": 3,
                    "distribution": {"a:barren_land": {"cell_count": 3}}
                },
                "a:open_water": {
                    "cell_count": 2,
                    "distribution": {"a:open_water": {"cell_count": 2}}
                }
            }
        }

        actual = create_modified_census(census)
        self.assertEqual(actual, expected)

    def test_create_modified_census_2(self):
        """
        create_modified_census from a census w/ trivial modifications.
        """
        census = {
            "cell_count": 3,
            "distribution": {
                "a:barren_land": {"cell_count": 2},
                "a:open_water": {"cell_count": 1}
            },
            "modifications": []
        }

        expected = {
            "cell_count": 3,
            "distribution": {
                "a:barren_land": {
                    "cell_count": 2,
                    "distribution": {"a:barren_land": {"cell_count": 2}}
                },
                "a:open_water": {
                    "cell_count": 1,
                    "distribution": {"a:open_water": {"cell_count": 1}}
                }
            }
        }

        actual = create_modified_census(census)
        self.assertEqual(actual, expected)

    def test_create_modified_census_3(self):
        """
        create_modified_census with non-trivial modifications.
        """
        census = {
            "cell_count": 144,
            "distribution": {
                "a:barren_land": {"cell_count": 55},
                "a:open_water": {"cell_count": 89}
            },
            "modifications": [
                {
                    "change": "::cluster_housing",
                    "cell_count": 34,
                    "distribution": {
                        "a:barren_land": {"cell_count": 34}
                    }
                }
            ]
        }

        expected = {
            "cell_count": 144,
            "distribution": {
                "a:barren_land": {
                    "cell_count": 55,
                    "distribution": {
                        "a:barren_land:cluster_housing": {"cell_count": 34},
                        "a:barren_land": {"cell_count": 21}
                    }
                },
                "a:open_water": {
                    "cell_count": 89,
                    "distribution": {
                        "a:open_water": {"cell_count": 89}
                    }
                }
            }
        }

        actual = create_modified_census(census)
        self.assertEqual(actual, expected)

    def test_create_modified_census_4(self):
        """
        create_modified_census with different types of changes.
        """
        census = {
            "distribution": {
                "a:developed_low": {
                    "cell_count": 3
                }
            },
            "cell_count": 3,
            "modifications": [
                {
                    "distribution": {
                        "a:developed_low": {
                            "cell_count": 1
                        }
                    },
                    "cell_count": 1,
                    "change": ":deciduous_forest:cluster_housing"
                },
                {
                    "distribution": {
                        "a:developed_low": {
                            "cell_count": 1
                        }
                    },
                    "cell_count": 1,
                    "change": ":deciduous_forest:"
                },
                {
                    "distribution": {
                        "a:developed_low": {
                            "cell_count": 1
                        }
                    },
                    "cell_count": 1,
                    "change": "::cluster_housing"
                },
            ]
        }

        expected = set([
            'a:deciduous_forest:',
            'a:developed_low',
            'a:deciduous_forest:cluster_housing',
            'a:developed_low:cluster_housing'])
        modified = create_modified_census(census)
        distrib = modified['distribution']['a:developed_low']['distribution']
        actual = set(distrib.keys())
        self.assertEqual(actual, expected)

    def test_simulate_water_quality_1(self):
        """
        Test the water quality simulation with unmodified census.
        """
        census = {
            "cell_count": 5,
            "distribution": {
                "a:barren_land": {"cell_count": 3},
                "a:open_water": {"cell_count": 2}
            }
        }

        def fn(cell, cell_count):
            return simulate_cell_day(5, 0.207, cell, cell_count)

        simulate_water_quality(census, 93, fn)
        left = census['distribution']['a:barren_land']
        right = census['distribution']['a:open_water']
        for key in set(census.keys()) - set(['distribution']):
            self.assertEqual(left[key] + right[key], census[key])

    def test_simulate_water_quality_2(self):
        """
        Test the water quality simulation in the presence of modifications.
        """
        census = {
            "cell_count": 3,
            "distribution": {
                "a:barren_land": {"cell_count": 2},
                "a:open_water": {"cell_count": 1}
            },
            "modifications": [
                {
                    "change": "d:developed_med:",
                    "cell_count": 1,
                    "distribution": {
                        "a:barren_land": {"cell_count": 1}
                    }
                }
            ]
        }

        census1 = create_modified_census(census)
        census2 = {
            "cell_count": 3,
            "distribution": {
                "a:barren_land": {"cell_count": 1},
                "d:developed_med": {"cell_count": 1},
                "a:open_water": {"cell_count": 1}
            }
        }

        def fn(cell, cell_count):
            return simulate_cell_day(5, 0.207, cell, cell_count)

        simulate_water_quality(census1, 93, fn)
        simulate_water_quality(census2, 93, fn)
        for key in set(census1.keys()) - set(['distribution']):
            self.assertEqual(census1[key], census2[key])

    def test_simulate_water_quality_precolumbian(self):
        """
        Test the water quality simulation in Pre-Columbian times.
        """
        census1 = {
            "cell_count": 8,
            "distribution": {
                "a:developed_med": {"cell_count": 1},
                "b:no_till": {"cell_count": 1},
                "c:pasture": {"cell_count": 1},
                "d:cultivated_crops": {"cell_count": 1},
                "a:open_water": {"cell_count": 1},
                "b:shrub": {"cell_count": 1},
                "c:barren_land": {"cell_count": 1},
                "d:developed_open": {"cell_count": 1}
            }
        }

        census2 = {
            "cell_count": 8,
            "distribution": {
                "a:mixed_forest": {"cell_count": 1},
                "b:mixed_forest": {"cell_count": 1},
                "c:mixed_forest": {"cell_count": 1},
                "d:mixed_forest": {"cell_count": 2},
                "a:open_water": {"cell_count": 1},
                "b:shrub": {"cell_count": 1},
                "c:barren_land": {"cell_count": 1}
            }
        }

        census3 = census2.copy()

        def fn(cell, cell_count):
            return simulate_cell_day(7, 0.107, cell, cell_count)

        simulate_water_quality(census1, 93, fn, precolumbian=True)
        simulate_water_quality(census2, 93, fn, precolumbian=True)
        simulate_water_quality(census3, 93, fn, precolumbian=False)

        for key in set(census1.keys()) - set(['distribution']):
            self.assertAlmostEqual(census1[key], census2[key])

        for key in set(census1.keys()) - set(['distribution']):
            self.assertAlmostEqual(census2[key], census3[key])

    def test_day_1(self):
        """
        Test the simulate_day function with only land cover modifications.
        """
        self.maxDiff = None

        precip = 2
        actual = simulate_day(CENSUS_1, precip)
        expected = DAY_OUTPUT_1
        self.assertEqual(actual, expected)

    def test_day_2(self):
        """
        Test the simulate_day function with lots of BMPs.
        """
        self.maxDiff = None
        precip = 2
        actual = simulate_day(CENSUS_2, precip)
        expected = DAY_OUTPUT_2
        self.assertEqual(actual, expected)

    def test_day_with_invalid_census(self):
        """
        Test the simulate_day function with a census
        that has a modification census with a cover type
        that doesn't exist within the AoI census. This is
        invalid input. Each land cover type in a modification
        census must be represented in AoI census.
        """
        census = {
            'distribution': {
                'b:developed_med': {'cell_count': 400},
            },
            'cell_count': 400,
            'modifications': [
                {
                    'distribution': {
                        'b:developed_low': {'cell_count': 40}
                    },
                    'cell_count': 40,
                    'change': ':deciduous_forest:'
                },
            ]
        }

        precip = 3
        self.assertRaises(ValueError,
                          simulate_day, *(census, precip))

    def test_bmp_runoff(self):
        """
        Make sure that BMPs do not produce negative runoff.
        """
        census = {
            "cell_count": 1,
            "distribution": {
                "d:developed_med": {"cell_count": 1}
            },
            "modifications": [
                {
                    "change": "::green_roof",
                    "cell_count": 1,
                    "distribution": {
                        "d:developed_med": {"cell_count": 1}
                    }
                }
            ]
        }
        result = simulate_day(census, 0.984)
        self.assertTrue(result['modified']['runoff'] >= 0)

    def test_water_balance(self):
        """
        Make sure that R, ET, and I sum to precip with no modifications.
        """
        census = {
            "cell_count": 1,
            "distribution": {
                "d:developed_med": {"cell_count": 1}
            },
        }
        precip = 0.984
        result = simulate_day(census, precip)
        runoff = result['modified']['runoff']
        et = result['modified']['et']
        inf = result['modified']['inf']
        total = runoff + et + inf
        # self.assertAlmostEqual(total, precip)
        self.assertEqual(total, precip)

    def test_water_balance_1(self):
        """
        Make sure that R, ET, and I sum to precip with only land cover modifications.
        """

        precip = 2.362
        result = simulate_day(CENSUS_1, precip)
        runoff = result['modified']['runoff']
        et = result['modified']['et']
        inf = result['modified']['inf']
        total = runoff + et + inf
        # self.assertAlmostEqual(total, precip)
        self.assertEqual(total, precip)

    def test_water_balance_2(self):
        """
        Make sure that R, ET, and I sum to precip with with lots of BMPs.
        """

        precip = 4.429
        result = simulate_day(CENSUS_2, precip)
        runoff = result['modified']['runoff']
        et = result['modified']['et']
        inf = result['modified']['inf']
        total = runoff + et + inf
        # self.assertAlmostEqual(total, precip)
        self.assertEqual(total, precip)

    def test_compute_bmp_effect(self):
        """
        Test that the BMP reduction is working as expected.
        """
        # This is an abbreviated census without postpass for 3.2"
        # of rain on developed_med on soil type c
        mod_census = {
            'BMPs': {
                'porous_paving': 10,
                'infiltration_basin': 15
            },
            'cell_count': 100,
            'inf-vol': 90.44788778622261,
            'et-vol': 3.7259999999999995,
            'runoff-vol': 225.8261122137774,
        }

        precip = 3.2 # should fill basin but not porous paving
        m2_per_pixel = 10
        pct = compute_bmp_effect(mod_census, m2_per_pixel, precip)

        # No exception should be raised, no bmp effect given
        self.assertAlmostEqual(0.8121403161, pct)

    def test_compute_bmp_no_runoff(self):
        """
        Test that no runoff will not produce errors when computing BMP effects
        """
        census = {
            'runoff-vol': 0,
            'BMPs': {
                'green_roof': 1942
            }
        }

        # No exception should be raised, no bmp effect given
        self.assertEqual(0, compute_bmp_effect(census, 42, 0.393))

if __name__ == "__main__":
    unittest.main()
