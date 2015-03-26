"""
TR-55 tables
"""

from datetime import date

# The 'yearstart' key points to the date on which this year-long
# dataset starts.  The 'growingstart' and 'growingend' keys point to
# dates giving the respective start and end of growing season.  The
# value associated with the 'percipitation' key is a tuple of a number
# of consecutive days, and the amount of percipitation during that run
# of days.
SampleYear = {'yearStart': date(1, 10, 15), # Sample year starts on 10/15
              'daysPerYear': 365,           # The number of days in the sample year

              'growingStart': date(1, 4, 15), # Growing season starts on 4/15
              'growingEnd': date(1, 10, 14),  # The last day of growing season is 10/14
              'growingETmax': 0.207,          # Maximum evapotranspiration during growing season
              'nonGrowingETmax': 0.0,         # ditto non-growing season

              'precipitation' : [
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
                  (122, 0.00)]
}

TableA = {
    'Water':             0.0,
    'LI_Residential':    0.42,
    'HI_Residential':    0.18,
    'Commercial':        0.06,
    'Industrial':        0.06,
    'Transportation':    0.06,
    'Rock':              0.0,
    'Sand':              0.0,
    'Clay':              0.0,
    'DeciduousForest':   0.7,
    'EvergreenForest':   0.7,
    'MixedForest':       0.7,
    'Grassland':         0.6,
    'Pasture':           0.6,
    'Hay':               0.6,
    'RowCrop':           0.9,
    'UrbanGrass':        0.7,
    'WoodyWetland':      1,
    'HerbaceousWetland': 1,
    'GreenRoof':         0.4,
    'PorousPaving':      0.0,
    'RainGarden':        0.08,
    'InfiltrationTrench': 0.0
}

# Inches of retention for different BMPs on different soil types
TableB = {
    'soilA': {
        'GreenRoof':          1.6,
        'PorousPaving':       7.73,
        'RainGarden':         1.2,
        'InfiltrationTrench': 2.4
    },
    'soilB': {
        'GreenRoof':          1.6,
        'PorousPaving':       4.13,
        'RainGarden':         0.6,
        'InfiltrationTrench': 1.8
    },
    'soilC': {
        'GreenRoof':          1.6,
        'PorousPaving':       1.73,
        'RainGarden':         0.2,
        'InfiltrationTrench': 1.4
    },
    'soilD': {
        'GreenRoof': 1.6
    }
}

# The set of best management practices that we know about
BMPs = set(TableB['soilA'].keys())

# The set of "built" land uses
BuiltTypes = set(['LI_Residential', 'HI_Residential', 'Commercial', 'Industrial', 'Transportation', 'UrbanGrass'])

TableC = {
    'soilA': {
        'Water':             100,
        'LI_Residential':    51,
        'HI_Residential':    77,
        'Commercial':        89,
        'Industrial':        89,
        'Transportation':    89,
        'Rock':              77,
        'Sand':              77,
        'Clay':              77,
        'DeciduousForest':   30,
        'EvergreenForest':   30,
        'MixedForest':       30,
        'Grassland':         30,
        'Pasture':           39,
        'Hay':               39,
        'RowCrop':           67,
        'UrbanGrass':        68,
        'WoodyWetland':      98,
        'HerbaceousWetland': 98
    },
    'soilB': {
        'Water':             100,
        'LI_Residential':    68,
        'HI_Residential':    85,
        'Commercial':        92,
        'Industrial':        92,
        'Transportation':    92,
        'Rock':              86,
        'Sand':              86,
        'Clay':              86,
        'DeciduousForest':   55,
        'EvergreenForest':   55,
        'MixedForest':       55,
        'Grassland':         58,
        'Pasture':           61,
        'Hay':               61,
        'RowCrop':           78,
        'UrbanGrass':        79,
        'WoodyWetland':      98,
        'HerbaceousWetland': 98
    },
    'soilC': {
        'Water':             100,
        'LI_Residential':    79,
        'HI_Residential':    90,
        'Commercial':        94,
        'Industrial':        94,
        'Transportation':    94,
        'Rock':              86,
        'Sand':              86,
        'Clay':              86,
        'DeciduousForest':   70,
        'EvergreenForest':   70,
        'MixedForest':       70,
        'Grassland':         71,
        'Pasture':           74,
        'Hay':               74,
        'RowCrop':           85,
        'UrbanGrass':        86,
        'WoodyWetland':      98,
        'HerbaceousWetland': 98
    },
    'soilD': {
        'Water':             100,
        'LI_Residential':    84,
        'HI_Residential':    92,
        'Commercial':        95,
        'Industrial':        95,
        'Transportation':    95,
        'Rock':              91,
        'Sand':              91,
        'Clay':              91,
        'DeciduousForest':   77,
        'EvergreenForest':   77,
        'MixedForest':       77,
        'Grassland':         78,
        'Pasture':           80,
        'Hay':               80,
        'RowCrop':           89,
        'UrbanGrass':        89,
        'WoodyWetland':      98,
        'HerbaceousWetland': 98
    }
}
