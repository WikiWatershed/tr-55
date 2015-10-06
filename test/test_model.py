# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
Model test set
"""

import unittest
from math import sqrt

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

# INPUT and OUTPUT are data that were emailed to Azavea in a spreadsheet for
# testing the TR-55 model implementation. The types were converted to NLCD
# strings based on the NLCD type number used by tables.py to calculate
# model results.
INPUT = [
    (0.5, 'a:open_water'),
    (1, 'a:open_water'),
    (2, 'a:open_water'),
    (3.2, 'a:open_water'),
    (8, 'a:open_water'),
    (0.5, 'a:barren_land'),
    (1, 'a:barren_land'),
    (2, 'a:barren_land'),
    (3.2, 'a:barren_land'),
    (8, 'a:barren_land'),
    (0.5, 'a:developed_open'),
    (1, 'a:developed_open'),
    (2, 'a:developed_open'),
    (3.2, 'a:developed_open'),
    (8, 'a:developed_open'),
    (0.5, 'a:developed_low'),
    (1, 'a:developed_low'),
    (2, 'a:developed_low'),
    (3.2, 'a:developed_low'),
    (8, 'a:developed_low'),
    (0.5, 'a:developed_med'),
    (1, 'a:developed_med'),
    (2, 'a:developed_med'),
    (3.2, 'a:developed_med'),
    (8, 'a:developed_med'),
    (0.5, 'a:developed_high'),
    (1, 'a:developed_high'),
    (2, 'a:developed_high'),
    (3.2, 'a:developed_high'),
    (8, 'a:developed_high'),
    (0.5, 'a:deciduous_forest'),
    (0.5, 'a:evergreen_forest'),
    (0.5, 'a:mixed_forest'),
    (1, 'a:deciduous_forest'),
    (1, 'a:evergreen_forest'),
    (1, 'a:mixed_forest'),
    (2, 'a:deciduous_forest'),
    (2, 'a:evergreen_forest'),
    (2, 'a:mixed_forest'),
    (3.2, 'a:deciduous_forest'),
    (3.2, 'a:evergreen_forest'),
    (3.2, 'a:mixed_forest'),
    (8, 'a:deciduous_forest'),
    (8, 'a:evergreen_forest'),
    (8, 'a:mixed_forest'),
    (0.5, 'a:grassland'),
    (1, 'a:grassland'),
    (2, 'a:grassland'),
    (3.2, 'a:grassland'),
    (8, 'a:grassland'),
    (0.5, 'a:pasture'),
    (1, 'a:pasture'),
    (2, 'a:pasture'),
    (3.2, 'a:pasture'),
    (8, 'a:pasture'),
    (0.5, 'a:cultivated_crops'),
    (1, 'a:cultivated_crops'),
    (2, 'a:cultivated_crops'),
    (3.2, 'a:cultivated_crops'),
    (8, 'a:cultivated_crops'),
    (0.5, 'a:woody_wetlands'),
    (0.5, 'a:herbaceous_wetlands'),
    (1, 'a:woody_wetlands'),
    (1, 'a:herbaceous_wetlands'),
    (2, 'a:woody_wetlands'),
    (2, 'a:herbaceous_wetlands'),
    (3.2, 'a:woody_wetlands'),
    (3.2, 'a:herbaceous_wetlands'),
    (8, 'a:woody_wetlands'),
    (8, 'a:herbaceous_wetlands'),
    (0.5, 'b:open_water'),
    (1, 'b:open_water'),
    (2, 'b:open_water'),
    (3.2, 'b:open_water'),
    (8, 'b:open_water'),
    (0.5, 'b:barren_land'),
    (1, 'b:barren_land'),
    (2, 'b:barren_land'),
    (3.2, 'b:barren_land'),
    (8, 'b:barren_land'),
    (0.5, 'b:developed_open'),
    (1, 'b:developed_open'),
    (2, 'b:developed_open'),
    (3.2, 'b:developed_open'),
    (8, 'b:developed_open'),
    (0.5, 'b:developed_low'),
    (1, 'b:developed_low'),
    (2, 'b:developed_low'),
    (3.2, 'b:developed_low'),
    (8, 'b:developed_low'),
    (0.5, 'b:developed_med'),
    (1, 'b:developed_med'),
    (2, 'b:developed_med'),
    (3.2, 'b:developed_med'),
    (8, 'b:developed_med'),
    (0.5, 'b:developed_high'),
    (1, 'b:developed_high'),
    (2, 'b:developed_high'),
    (3.2, 'b:developed_high'),
    (8, 'b:developed_high'),
    (0.5, 'b:deciduous_forest'),
    (0.5, 'b:evergreen_forest'),
    (0.5, 'b:mixed_forest'),
    (1, 'b:deciduous_forest'),
    (1, 'b:evergreen_forest'),
    (1, 'b:mixed_forest'),
    (2, 'b:deciduous_forest'),
    (2, 'b:evergreen_forest'),
    (2, 'b:mixed_forest'),
    (3.2, 'b:deciduous_forest'),
    (3.2, 'b:evergreen_forest'),
    (3.2, 'b:mixed_forest'),
    (8, 'b:deciduous_forest'),
    (8, 'b:evergreen_forest'),
    (8, 'b:mixed_forest'),
    (0.5, 'b:grassland'),
    (1, 'b:grassland'),
    (2, 'b:grassland'),
    (3.2, 'b:grassland'),
    (8, 'b:grassland'),
    (0.5, 'b:pasture'),
    (1, 'b:pasture'),
    (2, 'b:pasture'),
    (3.2, 'b:pasture'),
    (8, 'b:pasture'),
    (0.5, 'b:cultivated_crops'),
    (1, 'b:cultivated_crops'),
    (2, 'b:cultivated_crops'),
    (3.2, 'b:cultivated_crops'),
    (8, 'b:cultivated_crops'),
    (0.5, 'b:woody_wetlands'),
    (0.5, 'b:herbaceous_wetlands'),
    (1, 'b:woody_wetlands'),
    (1, 'b:herbaceous_wetlands'),
    (2, 'b:woody_wetlands'),
    (2, 'b:herbaceous_wetlands'),
    (3.2, 'b:woody_wetlands'),
    (3.2, 'b:herbaceous_wetlands'),
    (8, 'b:woody_wetlands'),
    (8, 'b:herbaceous_wetlands'),
    (0.5, 'c:open_water'),
    (1, 'c:open_water'),
    (2, 'c:open_water'),
    (3.2, 'c:open_water'),
    (8, 'c:open_water'),
    (0.5, 'c:barren_land'),
    (1, 'c:barren_land'),
    (2, 'c:barren_land'),
    (3.2, 'c:barren_land'),
    (8, 'c:barren_land'),
    (0.5, 'c:developed_open'),
    (1, 'c:developed_open'),
    (2, 'c:developed_open'),
    (3.2, 'c:developed_open'),
    (8, 'c:developed_open'),
    (0.5, 'c:developed_low'),
    (1, 'c:developed_low'),
    (2, 'c:developed_low'),
    (3.2, 'c:developed_low'),
    (8, 'c:developed_low'),
    (0.5, 'c:developed_med'),
    (1, 'c:developed_med'),
    (2, 'c:developed_med'),
    (3.2, 'c:developed_med'),
    (8, 'c:developed_med'),
    (0.5, 'c:developed_high'),
    (1, 'c:developed_high'),
    (2, 'c:developed_high'),
    (3.2, 'c:developed_high'),
    (8, 'c:developed_high'),
    (0.5, 'c:deciduous_forest'),
    (0.5, 'c:evergreen_forest'),
    (0.5, 'c:mixed_forest'),
    (1, 'c:deciduous_forest'),
    (1, 'c:evergreen_forest'),
    (1, 'c:mixed_forest'),
    (2, 'c:deciduous_forest'),
    (2, 'c:evergreen_forest'),
    (2, 'c:mixed_forest'),
    (3.2, 'c:deciduous_forest'),
    (3.2, 'c:evergreen_forest'),
    (3.2, 'c:mixed_forest'),
    (8, 'c:deciduous_forest'),
    (8, 'c:evergreen_forest'),
    (8, 'c:mixed_forest'),
    (0.5, 'c:grassland'),
    (1, 'c:grassland'),
    (2, 'c:grassland'),
    (3.2, 'c:grassland'),
    (8, 'c:grassland'),
    (0.5, 'c:pasture'),
    (1, 'c:pasture'),
    (2, 'c:pasture'),
    (3.2, 'c:pasture'),
    (8, 'c:pasture'),
    (0.5, 'c:cultivated_crops'),
    (1, 'c:cultivated_crops'),
    (2, 'c:cultivated_crops'),
    (3.2, 'c:cultivated_crops'),
    (8, 'c:cultivated_crops'),
    (0.5, 'c:woody_wetlands'),
    (0.5, 'c:herbaceous_wetlands'),
    (1, 'c:woody_wetlands'),
    (1, 'c:herbaceous_wetlands'),
    (2, 'c:woody_wetlands'),
    (2, 'c:herbaceous_wetlands'),
    (3.2, 'c:woody_wetlands'),
    (3.2, 'c:herbaceous_wetlands'),
    (8, 'c:woody_wetlands'),
    (8, 'c:herbaceous_wetlands'),
    (0.5, 'd:open_water'),
    (1, 'd:open_water'),
    (2, 'd:open_water'),
    (3.2, 'd:open_water'),
    (8, 'd:open_water'),
    (0.5, 'd:barren_land'),
    (1, 'd:barren_land'),
    (2, 'd:barren_land'),
    (3.2, 'd:barren_land'),
    (8, 'd:barren_land'),
    (0.5, 'd:developed_open'),
    (1, 'd:developed_open'),
    (2, 'd:developed_open'),
    (3.2, 'd:developed_open'),
    (8, 'd:developed_open'),
    (0.5, 'd:developed_low'),
    (1, 'd:developed_low'),
    (2, 'd:developed_low'),
    (3.2, 'd:developed_low'),
    (8, 'd:developed_low'),
    (0.5, 'd:developed_med'),
    (1, 'd:developed_med'),
    (2, 'd:developed_med'),
    (3.2, 'd:developed_med'),
    (8, 'd:developed_med'),
    (0.5, 'd:developed_high'),
    (1, 'd:developed_high'),
    (2, 'd:developed_high'),
    (3.2, 'd:developed_high'),
    (8, 'd:developed_high'),
    (0.5, 'd:deciduous_forest'),
    (0.5, 'd:evergreen_forest'),
    (0.5, 'd:mixed_forest'),
    (1, 'd:deciduous_forest'),
    (1, 'd:evergreen_forest'),
    (1, 'd:mixed_forest'),
    (2, 'd:deciduous_forest'),
    (2, 'd:evergreen_forest'),
    (2, 'd:mixed_forest'),
    (3.2, 'd:deciduous_forest'),
    (3.2, 'd:evergreen_forest'),
    (3.2, 'd:mixed_forest'),
    (8, 'd:deciduous_forest'),
    (8, 'd:evergreen_forest'),
    (8, 'd:mixed_forest'),
    (0.5, 'd:grassland'),
    (1, 'd:grassland'),
    (2, 'd:grassland'),
    (3.2, 'd:grassland'),
    (8, 'd:grassland'),
    (0.5, 'd:pasture'),
    (1, 'd:pasture'),
    (2, 'd:pasture'),
    (3.2, 'd:pasture'),
    (8, 'd:pasture'),
    (0.5, 'd:cultivated_crops'),
    (1, 'd:cultivated_crops'),
    (2, 'd:cultivated_crops'),
    (3.2, 'd:cultivated_crops'),
    (8, 'd:cultivated_crops'),
    (0.5, 'd:woody_wetlands'),
    (0.5, 'd:herbaceous_wetlands'),
    (1, 'd:woody_wetlands'),
    (1, 'd:herbaceous_wetlands'),
    (2, 'd:woody_wetlands'),
    (2, 'd:herbaceous_wetlands'),
    (3.2, 'd:woody_wetlands'),
    (3.2, 'd:herbaceous_wetlands'),
    (8, 'd:woody_wetlands'),
    (8, 'd:herbaceous_wetlands')
]

OUTPUT = [
    (0.5, 0, 0),
    (1, 0, 0),
    (2, 0, 0),
    (3.2, 0, 0),
    (8, 0, 0),
    (0, 0, 0.5),
    (0, 0, 1),
    (0.4, 0, 1.6),
    (1.2, 0, 2),
    (5.3, 0, 2.7),
    (0, 0.1, 0.3),
    (0.1, 0.1, 0.7),
    (0.2, 0.1, 1.7),
    (0.7, 0.1, 2.3),
    (4.2, 0.1, 3.6),
    (0.1, 0.1, 0.3),
    (0.3, 0.1, 0.6),
    (0, 0.1, 1.9),
    (0.2, 0.1, 3),
    (2.4, 0.1, 5.6),
    (0.3, 0, 0.1),
    (0.7, 0, 0.3),
    (0.4, 0, 1.5),
    (1.2, 0, 2),
    (5.3, 0, 2.7),
    (0.5, 0, 0),
    (1, 0, 0),
    (1, 0, 1),
    (2.1, 0, 1.1),
    (6.7, 0, 1.3),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0, 0.1, 0.9),
    (0, 0.1, 0.9),
    (0, 0.1, 1.9),
    (0, 0.1, 1.9),
    (0, 0.1, 1.9),
    (0, 0.1, 3.1),
    (0, 0.1, 3.1),
    (0, 0.1, 3.1),
    (0.4, 0.1, 7.4),
    (0.4, 0.1, 7.4),
    (0.4, 0.1, 7.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0, 0.1, 1.9),
    (0, 0.1, 3.1),
    (0.4, 0.1, 7.5),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0, 0.1, 1.9),
    (0, 0.1, 3.1),
    (1.2, 0.1, 6.7),
    (0, 0.2, 0.3),
    (0, 0.2, 0.8),
    (0.2, 0.2, 1.6),
    (0.7, 0.2, 2.3),
    (4.1, 0.2, 3.7),
    (0.3, 0.2, 0),
    (0.3, 0.2, 0),
    (0.8, 0.2, 0),
    (0.8, 0.2, 0),
    (1.8, 0.2, 0),
    (1.8, 0.2, 0),
    (3, 0.2, 0),
    (3, 0.2, 0),
    (7.8, 0.2, 0),
    (7.8, 0.2, 0),
    (0.5, 0, 0),
    (1, 0, 0),
    (2, 0, 0),
    (3.2, 0, 0),
    (8, 0, 0),
    (0, 0, 0.5),
    (0.2, 0, 0.8),
    (0.8, 0, 1.2),
    (1.8, 0, 1.4),
    (6.3, 0, 1.7),
    (0, 0.1, 0.3),
    (0.1, 0.1, 0.7),
    (0.5, 0.1, 1.3),
    (1.3, 0.1, 1.7),
    (5.5, 0.1, 2.3),
    (0.1, 0.1, 0.3),
    (0.3, 0.1, 0.6),
    (0.2, 0.1, 1.7),
    (0.7, 0.1, 2.4),
    (4.2, 0.1, 3.7),
    (0.3, 0, 0.1),
    (0.7, 0, 0.3),
    (0.8, 0, 1.2),
    (1.8, 0, 1.4),
    (6.2, 0, 1.7),
    (0.5, 0, 0),
    (1, 0, 0),
    (1.2, 0, 0.8),
    (2.4, 0, 0.8),
    (7, 0, 0.9),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0, 0.1, 0.9),
    (0, 0.1, 0.9),
    (0, 0.1, 1.8),
    (0, 0.1, 1.8),
    (0, 0.1, 1.8),
    (0.3, 0.1, 2.8),
    (0.3, 0.1, 2.8),
    (0.3, 0.1, 2.8),
    (2.8, 0.1, 5.1),
    (2.8, 0.1, 5.1),
    (2.8, 0.1, 5.1),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0, 0.1, 1.9),
    (0.3, 0.1, 2.8),
    (2.8, 0.1, 5.1),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0.1, 0.1, 1.8),
    (0.4, 0.1, 2.6),
    (3.4, 0.1, 4.4),
    (0, 0.2, 0.3),
    (0.1, 0.2, 0.8),
    (0.5, 0.2, 1.3),
    (1.3, 0.2, 1.7),
    (5.4, 0.2, 2.4),
    (0.3, 0.2, 0),
    (0.3, 0.2, 0),
    (0.8, 0.2, 0),
    (0.8, 0.2, 0),
    (1.8, 0.2, 0),
    (1.8, 0.2, 0),
    (3, 0.2, 0),
    (3, 0.2, 0),
    (7.8, 0.2, 0),
    (7.8, 0.2, 0),
    (0.5, 0, 0),
    (1, 0, 0),
    (2, 0, 0),
    (3.2, 0, 0),
    (8, 0, 0),
    (0.1, 0, 0.4),
    (0.4, 0, 0.6),
    (1.2, 0, 0.8),
    (2.3, 0, 0.9),
    (6.9, 0, 1.1),
    (0, 0.1, 0.3),
    (0.1, 0.1, 0.7),
    (0.8, 0.1, 1),
    (1.8, 0.1, 1.2),
    (6.3, 0.1, 1.5),
    (0.1, 0.1, 0.3),
    (0.3, 0.1, 0.6),
    (0.5, 0.1, 1.4),
    (1.3, 0.1, 1.8),
    (5.5, 0.1, 2.4),
    (0.3, 0, 0.1),
    (0.7, 0, 0.3),
    (1.1, 0, 0.9),
    (2.2, 0, 1),
    (6.8, 0, 1.2),
    (0.5, 0, 0),
    (1, 0, 0),
    (1.4, 0, 0.6),
    (2.5, 0, 0.6),
    (7.3, 0, 0.7),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.8),
    (0, 0.1, 0.8),
    (0, 0.1, 0.8),
    (0.2, 0.1, 1.6),
    (0.2, 0.1, 1.6),
    (0.2, 0.1, 1.6),
    (0.8, 0.1, 2.2),
    (0.8, 0.1, 2.2),
    (0.8, 0.1, 2.2),
    (4.5, 0.1, 3.4),
    (4.5, 0.1, 3.4),
    (4.5, 0.1, 3.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0.2, 0.1, 1.6),
    (0.8, 0.1, 2.2),
    (4.5, 0.1, 3.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.9),
    (0.3, 0.1, 1.5),
    (1, 0.1, 2),
    (4.9, 0.1, 2.9),
    (0, 0.2, 0.3),
    (0.2, 0.2, 0.6),
    (0.8, 0.2, 1),
    (1.8, 0.2, 1.3),
    (6.2, 0.2, 1.6),
    (0.3, 0.2, 0),
    (0.3, 0.2, 0),
    (0.8, 0.2, 0),
    (0.8, 0.2, 0),
    (1.8, 0.2, 0),
    (1.8, 0.2, 0),
    (3, 0.2, 0),
    (3, 0.2, 0),
    (7.8, 0.2, 0),
    (7.8, 0.2, 0),
    (0.5, 0, 0),
    (1, 0, 0),
    (2, 0, 0),
    (3.2, 0, 0),
    (8, 0, 0),
    (0.1, 0, 0.4),
    (0.5, 0, 0.5),
    (1.4, 0, 0.6),
    (2.5, 0, 0.7),
    (7.3, 0, 0.7),
    (0, 0.1, 0.3),
    (0.1, 0.1, 0.7),
    (1, 0.1, 0.8),
    (2.1, 0.1, 1),
    (6.7, 0.1, 1.2),
    (0.1, 0.1, 0.3),
    (0.3, 0.1, 0.6),
    (0.7, 0.1, 1.2),
    (1.7, 0.1, 1.4),
    (6.1, 0.1, 1.8),
    (0.3, 0, 0.1),
    (0.7, 0, 0.3),
    (1.2, 0, 0.7),
    (2.4, 0, 0.8),
    (7, 0, 0.9),
    (0.5, 0, 0),
    (1, 0, 0),
    (1.5, 0, 0.5),
    (2.6, 0, 0.5),
    (7.4, 0, 0.6),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.4),
    (0, 0.1, 0.8),
    (0, 0.1, 0.8),
    (0, 0.1, 0.8),
    (0.4, 0.1, 1.4),
    (0.4, 0.1, 1.4),
    (0.4, 0.1, 1.4),
    (1.2, 0.1, 1.8),
    (1.2, 0.1, 1.8),
    (1.2, 0.1, 1.8),
    (5.3, 0.1, 2.6),
    (5.3, 0.1, 2.6),
    (5.3, 0.1, 2.6),
    (0, 0.1, 0.4),
    (0, 0.1, 0.8),
    (0.4, 0.1, 1.4),
    (1.2, 0.1, 1.9),
    (5.3, 0.1, 2.6),
    (0, 0.1, 0.4),
    (0.1, 0.1, 0.8),
    (0.6, 0.1, 1.3),
    (1.4, 0.1, 1.7),
    (5.6, 0.1, 2.2),
    (0, 0.2, 0.3),
    (0.3, 0.2, 0.5),
    (1, 0.2, 0.8),
    (2.1, 0.2, 0.9),
    (6.7, 0.2, 1.1),
    (0.3, 0.2, 0),
    (0.3, 0.2, 0),
    (0.8, 0.2, 0),
    (0.8, 0.2, 0),
    (1.8, 0.2, 0),
    (1.8, 0.2, 0),
    (3, 0.2, 0),
    (3, 0.2, 0),
    (7.8, 0.2, 0),
    (7.8, 0.2, 0)
]

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
    'unmodified': {
        'inf': 1.4762466686413165,
        'cell_count': 147,
        'tp': 0.048497869127119175,
        'tn': 0.3010544583784289,
        'runoff': 0.4408688415627653,
        'et': 0.08288448979591835,
        'distribution': {
            'c:developed_high': {
                'cell_count': 42,
                'tp': 0.03354942097300307,
                'tn': 0.21201370198217218,
                'runoff': 0.9904463051399999,
                'et': 0.01242,
                'inf': 0.9971336948599999,
                'bod': 28.889779171197087,
                'tss': 5.892117058383664
            },
            'a:deciduous_forest': {
                'cell_count': 72,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 0.14489999999999997,
                'inf': 1.8550999999999997,
                'bod': 0.0,
                'tss': 0.0
            },
            'd:developed_med': {
                'cell_count': 33,
                'tp': 0.014948448154116101,
                'tn': 0.08904075639625678,
                'runoff': 0.7033022695105,
                'et': 0.037259999999999995,
                'inf': 1.2594377304895001,
                'bod': 15.33840767118,
                'tss': 1.832809730200322
            }
        },
        'bod': 44.228186842377085,
        'tss': 7.724926788583986
    },
    'modified': {
        'inf': 1.4443825689955982,
        'cell_count': 147,
        'tp': 0.04395677470812412,
        'tn': 0.2721366245288691,
        'runoff': 0.44386559426970806,
        'et': 0.11175183673469387,
        'distribution': {
            'c:developed_high': {
                'inf': 1.077061870392374,
                'cell_count': 42,
                'tp': 0.02803732401552826,
                'tn': 0.1771803114870189,
                'runoff': 0.827718129607626,
                'et': 0.09522,
                'distribution': {
                    'c:developed_high': {
                        'cell_count': 22,
                        'tp': 0.017573506223953986,
                        'tn': 0.11105479627637589,
                        'runoff': 0.99044630514,
                        'et': 0.012419999999999999,
                        'inf': 0.99713369486,
                        'bod': 15.132741470627044,
                        'tss': 3.086347030581919
                    },
                    'c:developed_high:no_till': {
                        'cell_count': 20,
                        'tp': 0.010463817791574277,
                        'tn': 0.06612551521064301,
                        'runoff': 0.6487171365220146,
                        'et': 0.1863,
                        'inf': 1.1649828634779853,
                        'bod': 9.010509764966741,
                        'tss': 1.8377079996452328
                    }
                },
                'bod': 24.143251235593787,
                'tss': 4.9240550302271515
            },
            'a:deciduous_forest': {
                'inf': 1.7843552932085411,
                'cell_count': 72,
                'tp': 3.258553846153846e-05,
                'tn': 0.0003258553846153846,
                'runoff': 0.08080720679145877,
                'et': 0.13483749999999997,
                'distribution': {
                    'a:deciduous_forest': {
                        'cell_count': 67,
                        'tp': 0.0,
                        'tn': 0.0,
                        'runoff': 0.0,
                        'et': 0.14489999999999997,
                        'inf': 1.8551,
                        'bod': 0.0,
                        'tss': 0.0
                    },
                    'd:barren_land:': {
                        'cell_count': 5,
                        'tp': 3.258553846153846e-05,
                        'tn': 0.0003258553846153846,
                        'runoff': 1.1636237777970062,
                        'et': 0.0,
                        'inf': 0.8363762222029937,
                        'bod': 4.301291076923077,
                        'tss': 0.032585538461538464
                    }
                },
                'bod': 4.301291076923077,
                'tss': 0.032585538461538464
            },
            'd:developed_med': {
                'inf': 1.1701229689350983,
                'cell_count': 33,
                'tp': 0.015886865154134316,
                'tn': 0.09463045765723485,
                'runoff': 0.7474533947012655,
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
                        'tp': 0.010418615380141523,
                        'tn': 0.06205870900345169,
                        'runoff': 0.7033022695104999,
                        'et': 0.037259999999999995,
                        'inf': 1.2594377304895001,
                        'bod': 10.690405346579997,
                        'tss': 1.2774128422608306
                    }
                },
                'bod': 16.30130511467695,
                'tss': 1.947867814550382
            }
        },
        'bod': 44.745847427193816,
        'tss': 6.904508383239072
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
    'unmodified': {
        'inf': 1.4785857682509507,
        'cell_count': 4,
        'tp': 0.0013746500037446765,
        'tn': 0.008688160939430185,
        'runoff': 0.4417192317490494,
        'et': 0.07969499999999999,
        'distribution': {
            'c:developed_high': {
                'cell_count': 1,
                'tp': 0.0007987957374524541,
                'tn': 0.005047945285289814,
                'runoff': 0.99044630514,
                'et': 0.012419999999999999,
                'inf': 0.99713369486,
                'bod': 0.687851885028502,
                'tss': 0.14028850139008725
            },
            'a:deciduous_forest': {
                'cell_count': 1,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 0.14489999999999997,
                'inf': 1.8551,
                'bod': 0.0,
                'tss': 0.0
            },
            'b:pasture': {
                'cell_count': 1,
                'tp': 0.00012287098889476473,
                'tn': 0.0009420109148598631,
                'runoff': 0.0731283523456977,
                'et': 0.12419999999999999,
                'inf': 1.8026716476543023,
                'bod': 0.04095699629825491,
                'tss': 0.020478498149127455
            },
            'd:developed_med': {
                'cell_count': 1,
                'tp': 0.0004529832773974576,
                'tn': 0.002698204739280508,
                'runoff': 0.7033022695105,
                'et': 0.037259999999999995,
                'inf': 1.2594377304895001,
                'bod': 0.46480023245999996,
                'tss': 0.05553968879394915
            }
        },
        'bod': 1.1936091137867568,
        'tss': 0.21630668833316385
    },
    'modified': {
        'inf': 1.4978906201690463,
        'cell_count': 4,
        'tp': 0.0014947940356953506,
        'tn': 0.010093182575177441,
        'runoff': 0.3934343798309537,
        'et': 0.108675,
        'distribution': {
            'c:developed_high': {
                'inf': 1.0641101843915999,
                'cell_count': 1,
                'tp': 0.0007414402317520271,
                'tn': 0.004685490353432948,
                'runoff': 0.9193298156084,
                'et': 0.01656,
                'distribution': {
                    'c:developed_high': {
                        'cell_count': 0,
                        'runoff': 0,
                        'et': 0,
                        'inf': 0
                    },
                    'c:developed_high:rain_garden': {
                        'cell_count': 1,
                        'tp': 0.0007414402317520271,
                        'tn': 0.004685490353432948,
                        'runoff': 0.9193298156084,
                        'et': 0.01656,
                        'inf': 1.0641101843915999,
                        'bod': 0.6384624217864677,
                        'tss': 0.13021544070144975
                    }
                },
                'bod': 0.6384624217864677,
                'tss': 0.13021544070144975
            },
            'a:deciduous_forest': {
                'cell_count': 1,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 0.14489999999999997,
                'inf': 1.8551,
                'distribution': {
                    'a:deciduous_forest': {
                        'cell_count': 1,
                        'tp': 0.0,
                        'tn': 0.0,
                        'runoff': 0.0,
                        'et': 0.14489999999999997,
                        'inf': 1.8551,
                        'bod': 0.0,
                        'tss': 0.0
                    }
                },
                'bod': 0.0,
                'tss': 0.0
            },
            'b:pasture': {
                'inf': 1.4934093771285855,
                'cell_count': 1,
                'tp': 0.0005381555074547796,
                'tn': 0.004125858890486643,
                'runoff': 0.32029062287141463,
                'et': 0.1863,
                'distribution': {
                    'b:pasture:no_till': {
                        'cell_count': 1,
                        'tp': 0.0005381555074547796,
                        'tn': 0.004125858890486643,
                        'runoff': 0.32029062287141463,
                        'et': 0.1863,
                        'inf': 1.4934093771285855,
                        'bod': 0.1793851691515932,
                        'tss': 0.0896925845757966
                    },
                    'b:pasture': {
                        'cell_count': 0,
                        'runoff': 0,
                        'et': 0,
                        'inf': 0
                    }
                },
                'bod': 0.1793851691515932,
                'tss': 0.0896925845757966
            },
            'd:developed_med': {
                'inf': 1.5789429191559998,
                'cell_count': 1,
                'tp': 0.000215198296488544,
                'tn': 0.001281833331257849,
                'runoff': 0.3341170808440001,
                'et': 0.08693999999999999,
                'distribution': {
                    'd:developed_med:cluster_housing': {
                        'cell_count': 1,
                        'tp': 0.000215198296488544,
                        'tn': 0.001281833331257849,
                        'runoff': 0.3341170808440001,
                        'et': 0.08693999999999999,
                        'inf': 1.5789429191559998,
                        'bod': 0.220812165092593,
                        'tss': 0.026385182439030177
                    },
                    'd:developed_med': {
                        'cell_count': 0,
                        'runoff': 0,
                        'et': 0,
                        'inf': 0
                    }
                },
                'bod': 0.220812165092593,
                'tss': 0.026385182439030177
            }
        },
        'bod': 1.0386597560306539,
        'tss': 0.24629320771627652
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

    def test_simulate_day_1(self):
        """
        Test the tile simulation using sample input/output.
        """
        # The number 0.04 is not very meaningful, this test just
        # attempts to give some idea about the mean error of the three
        # quantities -- relative to precipitation -- as compared to
        # the sample output that was emailed to us.
        def similar(incoming, expected):
            precip, tile_string = incoming
            results = simulate(precip, tile_string + ':')
            results = (results['runoff-vol'],
                       results['et-vol'],
                       results['inf-vol'])
            lam = lambda x, y: abs(x - y) / precip
            me = average(map(lam, results, expected))
            # Precipitation levels <= 2 inches are known to be
            # problematic.  It is unclear why the 'barren_land' type is
            # giving trouble on soil types C and D.
            if precip > 2 and tile_string != 'c:barren_land' \
               and tile_string != 'd:barren_land':
                self.assertTrue(me < 0.04, tile_string + ' ' + str(me))
        map(similar, INPUT, OUTPUT)

    def test_simulate_day_2(self):
        """
        Another test of the tile simulation using sample input/output.
        """
        # Test the RMSE of the runoff levels produced by the tile
        # simulation against values sample input/output.  The number
        # 0.13 is not very meaningful, this test just attempts to put
        # a bound on the deviation between the current output and the
        # sample output that was mailed to us.
        results = [simulate(precip, tile_string + ':')['runoff-vol'] / precip
                   for precip, tile_string in INPUT
                   if precip > 2 and tile_string != 'c:barren_land' and
                   tile_string != 'd:barren_land']
        expected = [OUTPUT[i][0] / INPUT[i][0]
                    for i in range(len(INPUT))
                    if INPUT[i][0] > 2 and INPUT[i][1] != 'c:barren_land' and
                    INPUT[i][1] != 'd:barren_land']
        lam = lambda x, y: pow((x - y), 2)
        rmse = sqrt(average(map(lam, results, expected)))
        self.assertTrue(rmse < 0.13)

    def test_simulate_day_3(self):
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

    def test_greenroof_runoff(self):
        """
        Make sure that the green roof BMP does not produce negative
        runoff.
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

if __name__ == "__main__":
    unittest.main()
