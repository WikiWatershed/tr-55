"""
TR-55 tables
"""

from datetime import date

# The 'year_start' key points to the date on which this year-long
# dataset starts.  The 'growing_start' and 'growing_end' keys point to
# dates giving the respective start and end of growing season.  The
# values in the array associated with the 'precipitation' key are
# tuples of a number of consecutive days, and the amount of
# precipitation during that run of days.
SAMPLE_YEAR = {
    'year_start': date(1, 10, 15),    # Sample year starts on 10/15
    'days_per_year': 365,             # The number of days in the sample year

    'growing_start': date(1, 4, 15),  # Growing season starts on 4/15
    'growing_end': date(1, 10, 14),   # The last day of growing season is 10/14
    'growing_etmax': 0.207,           # Max. e/t during growing season
    'nongrowing_etmax': 0.0,          # ditto non-growing season

    'precipitation': [
        (120, 0.00),
        (7, 0.01),
        (4, 0.02),
        (3, 0.03),
        (2, 0.04),
        (2, 0.05),
        (2, 0.06),
        (2, 0.07),
        (1, 0.08),
        (2, 0.09),
        (1, 0.10),
        (2, 0.11),
        (1, 0.12),
        (1, 0.14),
        (1, 0.15),
        (1, 0.16),
        (1, 0.17),
        (1, 0.18),
        (1, 0.20),
        (1, 0.21),
        (1, 0.23),
        (1, 0.25),
        (1, 0.26),
        (1, 0.28),
        (1, 0.30),
        (1, 0.33),
        (1, 0.34),
        (1, 0.37),
        (1, 0.38),
        (1, 0.41),
        (1, 0.44),
        (1, 0.48),
        (1, 0.52),
        (1, 0.55),
        (1, 0.59),
        (1, 0.63),
        (1, 0.67),
        (1, 0.72),
        (1, 0.77),
        (1, 0.82),
        (1, 0.89),
        (1, 0.98),
        (1, 1.09),
        (1, 1.22),
        (1, 1.42),
        (1, 1.92),

        (1, 2.71),
        (1, 1.88),
        (1, 1.57),
        (1, 1.33),
        (1, 1.18),
        (1, 1.06),
        (1, 0.95),
        (1, 0.86),
        (1, 0.76),
        (1, 0.69),
        (1, 0.63),
        (1, 0.57),
        (1, 0.54),
        (1, 0.50),
        (1, 0.46),
        (1, 0.43),
        (1, 0.40),
        (1, 0.37),
        (1, 0.34),
        (1, 0.33),
        (1, 0.30),
        (1, 0.28),
        (1, 0.26),
        (1, 0.25),
        (1, 0.23),
        (1, 0.22),
        (1, 0.20),
        (1, 0.18),
        (1, 0.17),
        (1, 0.16),
        (1, 0.15),
        (1, 0.13),
        (1, 0.12),
        (1, 0.11),
        (2, 0.10),
        (1, 0.09),
        (2, 0.08),
        (2, 0.07),
        (1, 0.06),
        (2, 0.05),
        (3, 0.04),
        (3, 0.03),
        (4, 0.02),
        (7, 0.01),
        (122, 0.00)
    ]
}

# Land use descriptions may map to the same nlcd code and have the same values
# but could be handled differently in the model execution (ex, commercial,
# industrial, transportation). Describes the NLCD class value, the landscape
# factor (ki) and the Curve Numbers for each hydrologic soil group for that use
# type
# NOTE: Missing NLCD types 12 & 52 (plus all Alaska only types (51, 72-74)
LAND_USE_VALUES = {
    'water':                {'nlcd': 11, 'ki': 0.0, 'cn': {'a': 100, 'b': 100, 'c': 100, 'd': 100}},  # noqa
    'li_residential':       {'nlcd': 22, 'ki': 0.42, 'cn': {'a': 51, 'b': 68, 'c': 79, 'd': 84}},  # noqa
    'hi_residential':       {'nlcd': 23, 'ki': 0.18, 'cn': {'a': 77, 'b': 85, 'c': 90, 'd': 92}},  # noqa
    'commercial':           {'nlcd': 24, 'ki': 0.06, 'cn': {'a': 89, 'b': 92, 'c': 94, 'd': 95}},  # noqa
    'industrial':           {'nlcd': 24, 'ki': 0.06, 'cn': {'a': 89, 'b': 92, 'c': 94, 'd': 95}},  # noqa
    'transportation':       {'nlcd': 24, 'ki': 0.06, 'cn': {'a': 89, 'b': 92, 'c': 94, 'd': 95}},  # noqa
    'rock':                 {'nlcd': 31, 'ki': 0.0, 'cn': {'a': 77, 'b': 86, 'c': 86, 'd': 91}},  # noqa
    'sand':                 {'nlcd': 31, 'ki': 0.0, 'cn': {'a': 77, 'b': 86, 'c': 86, 'd': 91}},  # noqa
    'clay':                 {'nlcd': 31, 'ki': 0.0, 'cn': {'a': 77, 'b': 86, 'c': 86, 'd': 91}},  # noqa
    'deciduous_forest':     {'nlcd': 41, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},  # noqa
    'evergreen_forest':     {'nlcd': 42, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},  # noqa
    'mixed_forest':         {'nlcd': 43, 'ki': 0.7, 'cn': {'a': 30, 'b': 55, 'c': 70, 'd': 77}},  # noqa
    'grassland':            {'nlcd': 71, 'ki': 0.6, 'cn': {'a': 30, 'b': 58, 'c': 71, 'd': 78}},  # noqa
    'pasture':              {'nlcd': 81, 'ki': 0.6, 'cn': {'a': 39, 'b': 61, 'c': 74, 'd': 80}},  # noqa
    'hay':                  {'nlcd': 81, 'ki': 0.6, 'cn': {'a': 39, 'b': 61, 'c': 74, 'd': 80}},  # noqa
    'row_crop':             {'nlcd': 82, 'ki': 0.9, 'cn': {'a': 67, 'b': 78, 'c': 85, 'd': 89}},  # noqa
    'urban_grass':          {'nlcd': 21, 'ki': 0.7, 'cn': {'a': 68, 'b': 79, 'c': 86, 'd': 89}},  # noqa
    'woody_wetland':        {'nlcd': 90, 'ki': 1, 'cn': {'a': 98, 'b': 98, 'c': 98, 'd': 98}},  # noqa
    'herbaceous_wetland':   {'nlcd': 95, 'ki': 1, 'cn': {'a': 98, 'b': 98, 'c': 98, 'd': 98}},  # noqa

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
BUILT_TYPES = set(['li_residential', 'hi_residential', 'cluster_housing',
                   'commercial', 'industrial', 'transportation',
                   'urban_grass'])

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
