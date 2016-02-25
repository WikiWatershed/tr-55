# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
TR-55 tables
"""


# For the different land uses, this describes the NLCD class value, the landscape factor (ki) and the Curve
# Numbers for each hydrologic soil group for that use type.
# NOTE: Missing NLCD type 12 (plus all Alaska only types (51, 72-74))
# For the BMP's the numbers are not Curve Numbers, they are quantities of rainfall (in inches)
#  that will be converted to infiltration by that BMP for that soil type.
LAND_USE_VALUES = {

		# NRCS Curve Numbers for NLCD land classes
    'open_water':           {'nlcd': 11, 'ki': 0.0, 'cn': {'a': 100, 'b': 100, 'c': 100, 'd': 100}},
        # Curve Number Source:  Assumes 100% runoff
        # Ki Source:
#    'perennial_ice':        {'nlcd': 12, 'ki': 0.0, 'cn': {'a': 100, 'b': 100, 'c': 100, 'd': 100}},
        # Curve Number Source:  Assumes 100% runoff
        # Ki Source:
    'developed_open':       {'nlcd': 21, 'ki': 0.7, 'cn': {'a': 59, 'b': 75, 'c': 83, 'd': 87}},
        # Curve Number Source:  Blend of Pasture - medium and paved parking assuming 20% impervious.
            # (TR-55, 1986, Table 2-2a)
        # Ki Source:
    'developed_low':        {'nlcd': 22, 'ki': 0.42, 'cn': {'a': 68, 'b': 80, 'c': 86, 'd': 89}},
        # Curve Number Source:  Blend of Pasture - medium and paved parking assuming 38% impervious.
            # (TR-55, 1986, Table 2-2a)
        # Ki Source:
    'developed_med':        {'nlcd': 23, 'ki': 0.18, 'cn': {'a': 81, 'b': 88, 'c': 91, 'd': 93}},
        # Curve Number Source:  Blend of Pasture - medium and paved parking assuming 65% impervious.
            # (TR-55, 1986, Table 2-2a)
        # Ki Source:
    'developed_high':       {'nlcd': 24, 'ki': 0.06, 'cn': {'a': 91, 'b': 94, 'c': 95, 'd': 96}},
        # Curve Number Source:  Blend of Pasture - medium and paved parking assuming 85% impervious.
        # Ki Source:
    'barren_land':          {'nlcd': 31, 'ki': 0.0, 'cn': {'a': 77, 'b': 86, 'c': 91, 'd': 94}},
        # Curve Number Source:  Fallow, Bare soil; Newly graded areas (TR-55, 1986, Table 2-2a and 2-2b)
        # Ki Source:
    'deciduous_forest':     {'nlcd': 41, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},
        # Curve Number Source:  Woods, Good condition;
            # Woods are protected from grazing and litter and brush adequately cover the soil.
            # (TR-55, 1986, Table 2-2c)
        # Ki Source:
    'evergreen_forest':     {'nlcd': 42, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},
        # Curve Number Source:  Woods, Good condition;
            # Woods are protected from grazing and litter and brush adequately cover the soil.
            # (TR-55, 1986, Table 2-2c)
        # Ki Source:
    'mixed_forest':         {'nlcd': 43, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},
        # Curve Number Source:  Woods, Good condition;
            # Woods are protected from grazing and litter and brush adequately cover the soil.
            # (TR-55, 1986, Table 2-2c)
        # Ki Source:
    'shrub':                {'nlcd': 52, 'ki': 1, 'cn': {'a': 35, 'b': 56, 'c': 70, 'd': 77}},
        # Curve Number Source:  Brush, fair; 50-75% ground cover (TR-55, 1986, Table 2-2c)
        # Ki Source:
    'grassland':            {'nlcd': 71, 'ki': 0.6, 'cn': {'a': 30, 'b': 58, 'c': 71, 'd': 78}},
        # Curve Number Source:  Meadow - continuous grass, protected from grazing and generally mowed for hay.
            # (TR-55, 1986, Table 2-2c)
        # Ki Source:
    'pasture':              {'nlcd': 81, 'ki': 0.6, 'cn': {'a': 39, 'b': 61, 'c': 74, 'd': 80}},
        # Curve Number Source:  Pasture, good; >75% ground cover and not heavily grazed. (TR-55, 1986, Table 2-2c)
        # Ki Source:
    'cultivated_crops':     {'nlcd': 82, 'ki': 0.9, 'cn': {'a': 67, 'b': 78, 'c': 85, 'd': 89}},
        # Curve Number Source:  Row crops, straight rows, good condition (TR-55, 1986, Table 2-2b)
        # Ki Source:
    'woody_wetlands':       {'nlcd': 90, 'ki': 1, 'cn': {'a': 30, 'b': 30, 'c': 30, 'd': 30}},
        # Curve Number Source: UNKNOWN
        # Ki Source:
    'herbaceous_wetlands':  {'nlcd': 95, 'ki': 1, 'cn': {'a': 30, 'b': 30, 'c': 30, 'd': 30}},
        # Curve Number Source: UNKNOWN
        # Ki Source:

    # NRCS Curve Numbers for BMP's acting as land cover changes
    'cluster_housing':      {'ki': 0.42},
        # Ki Source:
    'no_till':              {'ki': 0.9, 'cn': {'a': 57, 'b': 73, 'c': 82, 'd': 86}},
        # Curve Number Source:  UNKNOWN
        # Ki Source:

    # Storage Capacities for Infiltration BMP's, in m3/m2
    'green_roof':           {'ki': 0.4,  'storage': 0.020},
        # Assume a simple extensive vegetated roof cover
        # Source:  PA stormwater manual 6.5.1
    'infiltration_trench':  {'ki': 0.0,  'storage': 0.610},
        # A large open area with no infiltration underneath and 2' of ponding depth
        # Source:  New Jersey stormwater manual
    'porous_paving':        {'ki': 0.0,  'storage': 0.267},
        # Assume pervious bituminous asphalt used as the paving surface
        # Sources:  PA stormwater manual 6.4.1, StormTech (http://www.stormtech.com/download_files/pdf/techsheet1.pdf),
        # http://www.construction.basf.us/features/view/pervious-pavements
    'rain_garden':          {'ki': 0.08, 'storage': 0.396},
        # Source:  PA stormwater manual 6.4.5
}

# The set of best management practices that we know about.  The
# cluster_housing and no_till types are excluded because they do not
# actively retain water.
BMPS = set(['green_roof', 'porous_paving',
            'rain_garden', 'infiltration_trench'])

# The set of "built" land uses
# These are the land uses to which the Pitt model will be applied at less than 2" of rain.
BUILT_TYPES = set(['developed_open', 'developed_low', 'developed_med',
                   'developed_high', 'cluster_housing'])

NON_NATURAL = set(['pasture', 'cultivated_crops', 'green_roof']) | set(['no_till']) | BMPS | BUILT_TYPES

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
