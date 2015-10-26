"""
Generates a table with the model output for different input values.
This table is used in the mini-app.
"""

from itertools import product
import csv
import sys

from tr55.model import simulate_day


def cm_to_inches(cm):
    return cm / 2.54


def inches_to_cm(inches):
    return inches * 2.54


if len(sys.argv) != 2:
    print 'Usage: python -m tr55.makeMiniAppTable csv_file_name'
    sys.exit()
else:
    csv_file_name = sys.argv[1]

with open(csv_file_name, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('P', 'land', 'soil', 'ET', 'I', 'R'))

    # values of inputs to the model
    precip_cm = [1, 3, 5, 8, 21]

    # The land uses in the original mini-app used non NLCD types
    # (residential, high intensity residential, commercial, etc.) These were
    # converted to the best matches from the NLCD types based on the NLCD
    # number being used for the calculations in tables.py.
    land_uses = [
        'open_water',
        'developed_open',
        'developed_low',
        'developed_med',
        'developed_high',
        'barren_land',
        'deciduous_forest',
        'shrub',
        'grassland',
        'pasture',
        'cultivated_crops',
        'woody_wetlands'
    ]

    soil_types = ['a', 'b', 'c', 'd']

    soil_type_map = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3
    }

    # For each input value, compute the model outputs for a
    # single day and tile.
    for precip, land_use, soil_type in product(precip_cm,
                                               land_uses,
                                               soil_types):
        cells = {
            'cell_count': 1,
            'distribution': {
                '%s:%s' % (soil_type, land_use): {'cell_count': 1}
            }
        }

        model_out = simulate_day(cells, cm_to_inches(precip))['unmodified']

        writer.writerow((precip,
                         land_use,
                         soil_type_map[soil_type],
                         inches_to_cm(model_out['et']),
                         inches_to_cm(model_out['inf']),
                         inches_to_cm(model_out['runoff'])))
