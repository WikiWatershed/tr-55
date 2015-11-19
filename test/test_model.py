# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
Model test set
"""

import unittest

from tr55.model import runoff_nrcs, \
    simulate_cell_day, simulate_water_quality, \
    create_unmodified_census, create_modified_census, \
    simulate_day
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
    "modified": {
        "bod": 67.66870431502203,
        "cell_count": 147,
        "distribution": {
            "a:deciduous_forest": {
                "bod": 5.1614500050486845,
                "cell_count": 72,
                "distribution": {
                    "a:deciduous_forest": {
                        "bod": 0,
                        "cell_count": 67,
                        "et": 0.14489999999999997,
                        "inf": 1.8551,
                        "runoff": 0,
                        "tn": 0,
                        "tp": 0,
                        "tss": 0
                    },
                    "d:barren_land:": {
                        "bod": 5.1614500050486845,
                        "cell_count": 5,
                        "et": 0,
                        "inf": 0.6036783267219616,
                        "runoff": 1.3963216732780384,
                        "tn": 0.0003910189397764155,
                        "tp": 0.000039101893977641545,
                        "tss": 0.03910189397764155
                    }
                },
                "et": 0.13483749999999997,
                "inf": 1.7681957171334695,
                "runoff": 0.09696678286653043,
                "tn": 0.0003910189397764155,
                "tp": 0.000039101893977641545,
                "tss": 0.03910189397764155
            },
            "c:developed_high": {
                "bod": 35.51554384871639,
                "cell_count": 42,
                "distribution": {
                    "c:developed_high": {
                        "bod": 26.505034083749653,
                        "cell_count": 22,
                        "et": 0.012419999999999999,
                        "inf": 0.2528108488309999,
                        "runoff": 1.734769151169,
                        "tn": 0.1945127501307434,
                        "tp": 0.030780039581128623,
                        "tss": 5.405744451435715
                    },
                    "c:developed_high:no_till": {
                        "bod": 9.010509764966741,
                        "cell_count": 20,
                        "et": 0.1863,
                        "inf": 1.1649828634779853,
                        "runoff": 0.6487171365220146,
                        "tn": 0.06612551521064301,
                        "tp": 0.010463817791574277,
                        "tss": 1.8377079996452328
                    }
                },
                "et": 0.09522,
                "inf": 0.6871784748533739,
                "runoff": 1.217601525146626,
                "tn": 0.2606382653413864,
                "tp": 0.0412438573727029,
                "tss": 7.243452451080948
            },
            "d:developed_med": {
                "bod": 26.991710461256947,
                "cell_count": 33,
                "distribution": {
                    "d:developed_med": {
                        "bod": 21.380810693159994,
                        "cell_count": 23,
                        "et": 0.037259999999999995,
                        "inf": 0.5561354609789999,
                        "runoff": 1.4066045390209998,
                        "tn": 0.12411741800690337,
                        "tp": 0.020837230760283047,
                        "tss": 2.5548256845216613
                    },
                    "d:developed_med:no_till": {
                        "bod": 5.610899768096954,
                        "cell_count": 10,
                        "et": 0.1863,
                        "inf": 0.9646990173599737,
                        "runoff": 0.8490009826400262,
                        "tn": 0.03257174865378317,
                        "tp": 0.005468249773992795,
                        "tss": 0.6704549722895514
                    }
                },
                "et": 0.08242363636363635,
                "inf": 0.6799425992762647,
                "runoff": 1.2376337643600988,
                "tn": 0.15668916666068655,
                "tp": 0.02630548053427584,
                "tss": 3.2252806568112127
            }
        },
        "et": 0.11175183673469387,
        "inf": 1.215031927575294,
        "runoff": 0.6732162356900119,
        "tn": 0.41771845094184934,
        "tp": 0.06758843980095638,
        "tss": 10.507835001869802
    },
    "unmodified": {
        "bod": 81.27733495679115,
        "cell_count": 147,
        "distribution": {
            "a:deciduous_forest": {
                "bod": 0,
                "cell_count": 72,
                "et": 0.14489999999999997,
                "inf": 1.8550999999999997,
                "runoff": 0,
                "tn": 0,
                "tp": 0,
                "tss": 0
            },
            "c:developed_high": {
                "bod": 50.60051961443115,
                "cell_count": 42,
                "et": 0.01242,
                "inf": 0.2528108488309999,
                "runoff": 1.734769151169,
                "tn": 0.37134252297687376,
                "tp": 0.058761893745791015,
                "tss": 10.320057589104549
            },
            "d:developed_med": {
                "bod": 30.67681534236,
                "cell_count": 33,
                "et": 0.037259999999999995,
                "inf": 0.5561354609789999,
                "runoff": 1.406604539021,
                "tn": 0.17808151279251355,
                "tp": 0.029896896308232203,
                "tss": 3.665619460400644
            }
        },
        "et": 0.08288448979591835,
        "inf": 1.1056988153959795,
        "runoff": 0.8114166948081021,
        "tn": 0.5494240357693874,
        "tp": 0.08865879005402322,
        "tss": 13.985677049505192
    }
}

CENSUS_2 = {
    'cell_count': 4,
    'distribution': {
        'd:developed_med': {'cell_count': 1},
        'c:developed_high': {'cell_count': 1},
        'a:deciduous_forest': {'cell_count': 1},
        'b:pasture': {'cell_count': 1}
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
        },
        {
            'change': '::rain_garden',
            'cell_count': 1,
            'distribution': {
                'c:developed_high': {'cell_count': 1}
            }
        }
    ]
}

DAY_OUTPUT_2 = {
    "modified": {
        "bod": 1.6502192351913143,
        "cell_count": 4,
        "distribution": {
            "a:deciduous_forest": {
                "bod": 0,
                "cell_count": 1,
                "distribution": {
                    "a:deciduous_forest": {
                        "bod": 0,
                        "cell_count": 1,
                        "et": 0.14489999999999997,
                        "inf": 1.8551,
                        "runoff": 0,
                        "tn": 0,
                        "tp": 0,
                        "tss": 0
                    }
                },
                "et": 0.14489999999999997,
                "inf": 1.8551,
                "runoff": 0,
                "tn": 0,
                "tp": 0,
                "tss": 0
            },
            "b:pasture": {
                "bod": 0.1793851691515932,
                "cell_count": 1,
                "distribution": {
                    "b:pasture": {
                        "cell_count": 0,
                        "et": 0,
                        "inf": 0,
                        "runoff": 0
                    },
                    "b:pasture:no_till": {
                        "bod": 0.1793851691515932,
                        "cell_count": 1,
                        "et": 0.1863,
                        "inf": 1.4934093771285855,
                        "runoff": 0.32029062287141463,
                        "tn": 0.004125858890486643,
                        "tp": 0.0005381555074547796,
                        "tss": 0.0896925845757966
                    }
                },
                "et": 0.1863,
                "inf": 1.4934093771285855,
                "runoff": 0.32029062287141463,
                "tn": 0.004125858890486643,
                "tp": 0.0005381555074547796,
                "tss": 0.0896925845757966
            },
            "c:developed_high": {
                "bod": 1.0292097358545353,
                "cell_count": 1,
                "distribution": {
                    "c:developed_high": {
                        "cell_count": 0,
                        "et": 0,
                        "inf": 0,
                        "runoff": 0
                    },
                    "c:developed_high:rain_garden": {
                        "bod": 1.0292097358545353,
                        "cell_count": 1,
                        "et": 0.01656,
                        "inf": 0.5014683687832001,
                        "runoff": 1.4819716312167999,
                        "tn": 0.007553071448609896,
                        "tp": 0.001195211306153654,
                        "tss": 0.20990898564323546
                    }
                },
                "et": 0.01656,
                "inf": 0.5014683687832001,
                "runoff": 1.4819716312167999,
                "tn": 0.007553071448609896,
                "tp": 0.001195211306153654,
                "tss": 0.20990898564323546
            },
            "d:developed_med": {
                "bod": 0.441624330185186,
                "cell_count": 1,
                "distribution": {
                    "d:developed_med": {
                        "cell_count": 0,
                        "et": 0,
                        "inf": 0,
                        "runoff": 0
                    },
                    "d:developed_med:cluster_housing": {
                        "bod": 0.441624330185186,
                        "cell_count": 1,
                        "et": 0.08693999999999999,
                        "inf": 1.2448258383119999,
                        "runoff": 0.6682341616880002,
                        "tn": 0.002563666662515698,
                        "tp": 0.000430396592977088,
                        "tss": 0.052770364878060354
                    }
                },
                "et": 0.08693999999999999,
                "inf": 1.2448258383119999,
                "runoff": 0.6682341616880002,
                "tn": 0.002563666662515698,
                "tp": 0.000430396592977088,
                "tss": 0.052770364878060354
            }
        },
        "et": 0.108675,
        "inf": 1.2737008960559462,
        "runoff": 0.6176241039440536,
        "tn": 0.014242597001612237,
        "tp": 0.0021637634065855213,
        "tss": 0.3523719350970924
    },
    "unmodified": {
        "bod": 2.17533173775233,
        "cell_count": 4,
        "distribution": {
            "a:deciduous_forest": {
                "bod": 0,
                "cell_count": 1,
                "et": 0.14489999999999997,
                "inf": 1.8551,
                "runoff": 0,
                "tn": 0,
                "tp": 0,
                "tss": 0
            },
            "b:pasture": {
                "bod": 0.04095699629825491,
                "cell_count": 1,
                "et": 0.12419999999999999,
                "inf": 1.8026716476543023,
                "runoff": 0.0731283523456977,
                "tn": 0.0009420109148598631,
                "tp": 0.00012287098889476473,
                "tss": 0.020478498149127455
            },
            "c:developed_high": {
                "bod": 1.204774276534075,
                "cell_count": 1,
                "et": 0.012419999999999999,
                "inf": 0.2528108488309999,
                "runoff": 1.734769151169,
                "tn": 0.008841488642306519,
                "tp": 0.0013990927082331193,
                "tss": 0.2457156568834416
            },
            "d:developed_med": {
                "bod": 0.9296004649199999,
                "cell_count": 1,
                "et": 0.037259999999999995,
                "inf": 0.5561354609789999,
                "runoff": 1.406604539021,
                "tn": 0.005396409478561016,
                "tp": 0.0009059665547949152,
                "tss": 0.1110793775878983
            }
        },
        "et": 0.07969499999999999,
        "inf": 1.1166794893660754,
        "runoff": 0.8036255106339244,
        "tn": 0.015179909035727399,
        "tp": 0.002427930251922799,
        "tss": 0.37727353262046737
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

        # This pair has CN=90
        runoffs = [round(runoff_nrcs(precip, 0.0, 'c', 'developed_med'), 2)
                   for precip in PS]
        self.assertEqual(runoffs, CN90)

    def test_simulate_day(self):
        """
        Daily simulation.
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
        Test the water quality simulation.
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
        Test the simulate_day function.
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

    def test_bmp_sum(self):
        """
        Make sure that runoff, evapotranspiration, and infiltration sum to
        precipitation.
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

        precip = 0.984
        result = simulate_day(census, precip)
        runoff = result['modified']['runoff']
        et = result['modified']['et']
        inf = result['modified']['inf']
        total = runoff + et + inf
        self.assertAlmostEqual(total, precip)

    def test_bmps_on_d(self):
        """
        Make sure that BMPS all work on soil type D.
        """
        census = {
            "cell_count": 2,
            "distribution": {
                "c:developed_med": {"cell_count": 1},
                "d:developed_med": {"cell_count": 1}
            },
            "modifications": [
                {
                    "change": "::porous_paving",
                    "cell_count": 1,
                    "distribution": {
                        "c:developed_med": {"cell_count": 1}
                    }
                },
                {
                    "change": "::porous_paving",
                    "cell_count": 1,
                    "distribution": {
                        "d:developed_med": {"cell_count": 1}
                    }
                }
            ]
        }

        # Porous Paving
        precip = 3.3
        result = simulate_day(census, precip)
        c_inf = result['modified']['distribution']['c:developed_med']['inf']
        d_inf = result['modified']['distribution']['d:developed_med']['inf']
        self.assertAlmostEqual(c_inf / 3, d_inf)

        # Rain Garden
        census['modifications'][0]['change'] = '::rain_garden'
        census['modifications'][1]['change'] = '::rain_garden'
        result = simulate_day(census, precip)
        c_inf = result['modified']['distribution']['c:developed_med']['inf']
        d_inf = result['modified']['distribution']['d:developed_med']['inf']
        self.assertLess(d_inf, c_inf)
        self.assertGreater(d_inf / c_inf, 0.5)

        # Infiltration Trench
        census['modifications'][0]['change'] = '::infiltration_trench'
        census['modifications'][1]['change'] = '::infiltration_trench'
        result = simulate_day(census, precip)
        c_inf = result['modified']['distribution']['c:developed_med']['inf']
        d_inf = result['modified']['distribution']['d:developed_med']['inf']
        self.assertAlmostEqual(c_inf / 3, d_inf)

if __name__ == "__main__":
    unittest.main()
