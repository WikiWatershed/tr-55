# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
TR-55 tables
"""


# Describes the NLCD class value, the landscape factor (ki) and the Curve
# Numbers for each hydrologic soil group for that use type.
# NOTE: Missing NLCD type 12 (plus all Alaska only types (51, 72-74)
LAND_USE_VALUES = {
    'open_water':           {'nlcd': 11, 'ki': 0.0, 'cn': {'a': 100, 'b': 100, 'c': 100, 'd': 100}},  # noqa
#    'perennial_ice':        {'nlcd': 12, 'ki': 0.0, 'cn': {'a': 100, 'b': 100, 'c': 100, 'd': 100}},  # noqa
    'developed_open':       {'nlcd': 21, 'ki': 0.7, 'cn': {'a': 68, 'b': 79, 'c': 86, 'd': 89}},  # noqa
    'developed_low':        {'nlcd': 22, 'ki': 0.42, 'cn': {'a': 51, 'b': 68, 'c': 79, 'd': 84}},  # noqa
    'developed_med':        {'nlcd': 23, 'ki': 0.18, 'cn': {'a': 77, 'b': 85, 'c': 90, 'd': 92}},  # noqa
    'developed_high':       {'nlcd': 24, 'ki': 0.06, 'cn': {'a': 89, 'b': 92, 'c': 94, 'd': 95}},  # noqa
    'barren_land':          {'nlcd': 31, 'ki': 0.0, 'cn': {'a': 77, 'b': 86, 'c': 86, 'd': 91}},  # noqa
    'deciduous_forest':     {'nlcd': 41, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},  # noqa
    'evergreen_forest':     {'nlcd': 42, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},  # noqa
    'mixed_forest':         {'nlcd': 43, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},  # noqa
    'shrub':                {'nlcd': 52, 'ki': 1, 'cn': {'a': 35, 'b': 56, 'c': 70, 'd': 77}},  # noqa
    'grassland':            {'nlcd': 71, 'ki': 0.6, 'cn': {'a': 30, 'b': 58, 'c': 71, 'd': 78}},  # noqa
    'pasture':              {'nlcd': 81, 'ki': 0.6, 'cn': {'a': 39, 'b': 61, 'c': 74, 'd': 80}},  # noqa
    'cultivated_crops':     {'nlcd': 82, 'ki': 0.9, 'cn': {'a': 67, 'b': 78, 'c': 85, 'd': 89}},  # noqa
    'woody_wetlands':       {'nlcd': 90, 'ki': 1, 'cn': {'a': 98, 'b': 98, 'c': 98, 'd': 98}},  # noqa
    'herbaceous_wetlands':  {'nlcd': 95, 'ki': 1, 'cn': {'a': 98, 'b': 98, 'c': 98, 'd': 98}},  # noqa

    'green_roof':           {'ki': 0.4, 'infiltration': {'a': 1.6, 'b': 1.6, 'c': 1.6, 'd': 1.6}},  # noqa
    'porous_paving':        {'ki': 0.0, 'infiltration': {'a': 7.73, 'b': 4.13, 'c': 1.73}},  # noqa
    'rain_garden':          {'ki': 0.08, 'infiltration': {'a': 1.2, 'b': 0.6, 'c': 0.2}},  # noqa
    'infiltration_trench':  {'ki': 0.0, 'infiltration': {'a': 2.4, 'b': 1.8, 'c': 1.4}},  # noqa
    'cluster_housing':      {'ki': 0.42},
    'no_till':              {'ki': 0.9, 'cn': {'a': 57, 'b': 73, 'c': 82, 'd': 86}}  # noqa
}

# The set of best management practices that we know about.  The
# cluster_housing and no_till types are excluded because they do not
# actively retain water.
BMPS = set(['green_roof', 'porous_paving',
            'rain_garden', 'infiltration_trench'])

# The set of "built" land uses
BUILT_TYPES = set(['developed_low', 'developed_med', 'cluster_housing',
                   'developed_high'])

NON_NATURAL = set(['pasture', 'cultivated_crops', 'green_roof',
                   'developed_open']) | set(['no_till']) | BMPS | BUILT_TYPES

# The set of pollutants that we are concerned with.
POLLUTANTS = set(['tn', 'tp', 'bod', 'tss'])

# Event mean concentrations (mg/l) by pollutant and NLCD type
# tn: Total Nitrogen, tp: Total Phosphorus,
# bod: Biochemical Oxygen Demand, tss: Total Suspended Solids
POLLUTION_LOADS = {
    11: {'tn': 0,    'tp': 0,     'bod': 0,     'tss': 0},
    12: {'tn': 0,    'tp': 0,     'bod': 0,     'tss': 0},
    21: {'tn': 2.8,  'tp': 0.62,  'bod': 61,    'tss': 155.6},
    22: {'tn': 4.15, 'tp': 0.8,   'bod': 309,   'tss': 147.1},
    23: {'tn': 6.85, 'tp': 1.15,  'bod': 1180,  'tss': 141.0},
    24: {'tn': 9.1,  'tp': 1.44,  'bod': 1240,  'tss': 252.9},
    31: {'tn': 0.1,  'tp': 0.01,  'bod': 1320,  'tss': 10},
    32: {'tn': 0.1,  'tp': 0.01,  'bod': 30,    'tss': 10},
    41: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 39},
    42: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 39},
    43: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 39},
    51: {'tn': 0,    'tp': 0,     'bod': 0,     'tss': 0},
    52: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 39},
    71: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 47},
    72: {'tn': 0,    'tp': 0,     'bod': 0,     'tss': 0},
    73: {'tn': 0,    'tp': 0,     'bod': 0,     'tss': 0},
    74: {'tn': 0,    'tp': 0,     'bod': 0,     'tss': 0},
    81: {'tn': 23.0, 'tp': 3.0,   'bod': 1000,  'tss': 500},
    82: {'tn': 23.0, 'tp': 3.0,   'bod': 1000,  'tss': 1000},
    90: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    91: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    92: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    93: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    94: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    95: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    96: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    97: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    98: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0},
    99: {'tn': 0.19, 'tp': 0.006, 'bod': 61,    'tss': 0}
}
