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
        # Curve Number Source: Uses lowest curve numbers possible to maximize infiltration
        # Ki Source:
    'herbaceous_wetlands':  {'nlcd': 95, 'ki': 1, 'cn': {'a': 30, 'b': 30, 'c': 30, 'd': 30}},
        # Curve Number Source: Uses lowest curve numbers possible to maximize infiltration
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

# Runoff tables for Pitt's Small Storm Hydrology (SSH) model

    # The raw runoff coefficients are those measured by the USGS in Wisconsin
    # (Bannerman 1983, 1992 and 1993; Horwatich, 2004; Steuer 1996 and 1997; USEPA 1993; Walker 1994; Waschbusch 1999)
    # This data is also provided as the Rv (runoff coefficient) file for all regions *but* the SouthEast in version 10.x of WinSlamm    #
    # http://wi.water.usgs.gov/slamm/index.html
    # http://wi.water.usgs.gov/slamm/slamm_parameter_descriptions.htm
    # http://winslamm.com/Select_documentation.html    #
    #
    # The Standard Land Uses, including the percents of land in area type and their level of connectedness,
    #  are collected from multiple published papers analyzing different sites using WinSLAMM
    # Pitt has compiled all of the site summaries here:
    # http://winslamm.com/docs/Standard%20Land%20Use%20and%20Parameter%20file%20descriptions%20final%20April%2018%202011.pdf
    # The above pdf also lists the original sources of the raw data.    #
    #
    # The final runoff volumens and runoff ratios for each standard land use were calculated as the sum of the multiples of the raw runoff coefficients
    # for each area type and the percent of land in that area type in each standard land use.
    #
    # For this work, this is the mapping used between the NLCD class and the SSH's Standard Land Use:
    #    NLCD class 21 (Developed, Open) = "Open Space"
    #    NLCD class 22 (Developed, Low) = "Residential"
    #    NLCD class 23 (Developed, Medium) = "Institutional"
    #    NLCD class 24 (Developed, High) = "Commercial"

SSH_RAINFALL_STEPS = [0.01, 0.08, 0.12, 0.2, 0.39, 0.59, 0.79, 0.98, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.5, 3.9, 4.9]
SSH_RUNOFF_RATIOS = {
    'developed_open' :
         {'runoff_ratio':
              {'a': [0.0393,0.0472,0.0598,0.0645,0.1045,0.1272,0.1372,0.1432,0.1493,0.1558,0.1609,0.1637,0.1662,0.1686,0.1711,0.1726,0.1757],
               'b': [0.0393,0.0472,0.0598,0.0645,0.1177,0.1462,0.1636,0.1697,0.1809,0.1874,0.3127,0.3148,0.3165,0.3182,0.3199,0.3206,0.3229],
               'c': [0.0393,0.0472,0.0598,0.0645,0.1193,0.1528,0.1769,0.1904,0.2008,0.2423,0.3127,0.3148,0.3165,0.3182,0.3199,0.3624,0.4066],
               'd': [0.0393,0.0472,0.0598,0.0645,0.1193,0.1528,0.1769,0.1904,0.2008,0.2423,0.3127,0.3148,0.3165,0.3182,0.3199,0.3624,0.4066],
               }
         },
    'developed_low' :
         {'runoff_ratio':
              {'a' : [0.0785,0.1115,0.1437,0.1601,0.1841,0.2053,0.2138,0.2187,0.2249,0.2303,0.2359,0.2382,0.2412,0.2439,0.2465,0.2485,0.2523],
               'b' : [0.0785,0.1115,0.1437,0.1601,0.1960,0.2224,0.2377,0.2426,0.2534,0.2589,0.3731,0.3748,0.3770,0.3791,0.3809,0.3822,0.3853],
               'c' : [0.0785,0.1115,0.1437,0.1601,0.1974,0.2284,0.2496,0.2614,0.2714,0.3085,0.3731,0.3748,0.3770,0.3791,0.3809,0.4200,0.4609],
               'd' : [0.0785,0.1115,0.1437,0.1601,0.1974,0.2284,0.2496,0.2614,0.2714,0.3085,0.3731,0.3748,0.3770,0.3791,0.3809,0.4200,0.4609],
               }
         },
    'developed_med' :
         {'runoff_ratio':
              {'a' : [0.1322,0.1929,0.2631,0.3107,0.3698,0.4032,0.4235,0.4368,0.4521,0.4688,0.4816,0.4886,0.4953,0.5006,0.5047,0.5074,0.5138],
               'b' : [0.1322,0.1929,0.2631,0.3150,0.3838,0.4226,0.4474,0.4616,0.4797,0.4980,0.5715,0.5803,0.5887,0.5944,0.6002,0.6045,0.6146],
               'c' : [0.1322,0.1929,0.2631,0.3150,0.3846,0.4258,0.4539,0.4717,0.4895,0.5249,0.5715,0.5803,0.5887,0.5944,0.6002,0.6248,0.6553],
               'd' : [0.1322,0.1929,0.2631,0.3150,0.3846,0.4258,0.4539,0.4717,0.4895,0.5249,0.5715,0.5803,0.5887,0.5944,0.6002,0.6248,0.6553],
               }
         },
    'developed_high' :
         {'runoff_ratio':
              {'a': [0.1966,0.2815,0.4034,0.4796,0.5549,0.6037,0.6311,0.6471,0.6675,0.6891,0.7063,0.7154,0.7257,0.7335,0.7389,0.7435,0.7533],
               'b': [0.1966,0.2815,0.4034,0.4895,0.5803,0.6343,0.6647,0.6818,0.7045,0.7274,0.7724,0.7820,0.7925,0.8005,0.8059,0.8104,0.8203],
               'c': [0.1966,0.2815,0.4034,0.4895,0.5807,0.6358,0.6677,0.6865,0.7090,0.7398,0.7724,0.7820,0.7925,0.8005,0.8059,0.8197,0.8390],
               'd': [0.1966,0.2815,0.4034,0.4895,0.5807,0.6358,0.6677,0.6865,0.7090,0.7398,0.7724,0.7820,0.7925,0.8005,0.8059,0.8197,0.8390],
               }
         },
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
