"""
Generates a table with the model output for different input values.
This table is used in the mini-app.
"""

from itertools import product
import csv
import sys

from tr55.model import simulate_modifications, simulate_cell_day
from tr55.tablelookup import lookup_ki

if len(sys.argv) != 2:
    print 'Usage: python -m tr55.makeMiniAppTable csv_file_name'
    sys.exit()
else:
    csv_file_name = sys.argv[1]

with open(csv_file_name, 'wb') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('P', 'land', 'soil', 'ET', 'I', 'R'))

    # values of inputs to the model
    precips = [0.5, 1.0, 2.0, 3.2, 8.0]

    # The land uses in the original mini-app were low intensity
    # residential, high intensity residential, commercial, grassland, forest,
    # turf grass, pasture, row crops. The closest matching to the values in
    # this implementation of TR-55 are the following:
    land_uses = [
        'li_residential',
        'hi_residential',
        'commercial',
        'grassland',
        'mixed_forest',
        'urban_grass',
        'pasture',
        'row_crop',
        'chaparral',
        'tall_grass_prairie',
        'short_grass_prairie',
        'desert'
    ]

    soil_types = ['a', 'b', 'c', 'd']

    et_max = 0.207
    pre_columbian = False

    # For each input value, compute the model outputs for a
    # single day and tile.
    for precip, land_use, soil_type in product(precips,
                                               land_uses,
                                               soil_types):
        cells = {
            'cell_count': 1,
            'distribution': {
                '%s:%s' % (soil_type, land_use): {'cell_count': 1}
            }
        }

        def fn(cell, cell_count):
            (soil_type, land_use) = cell.lower().split(':')
            et = et_max * lookup_ki(land_use)
            return simulate_cell_day((precip, et), cell, cell_count)

        model_out = (simulate_modifications(cells, fn=fn)
                     ['unmodified']['distribution'].values()[0])
        writer.writerow((precip, land_use,
                         soil_type, model_out['et'],
                         model_out['inf'], model_out['runoff']))
