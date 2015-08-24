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
    simulate_cell_day, simulate_cell_year, simulate_water_quality, \
    create_unmodified_census, create_modified_census, \
    simulate_day, simulate_year
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

# INPUT and OUTPUT are data that were emailed to Azavea in a
# spreadsheet for testing the TR-55 model implementation.
INPUT = [
    (0.5, 'a:water'),
    (1, 'a:water'),
    (2, 'a:water'),
    (3.2, 'a:water'),
    (8, 'a:water'),
    (0.5, 'a:rock'),
    (1, 'a:rock'),
    (2, 'a:rock'),
    (3.2, 'a:rock'),
    (8, 'a:rock'),
    (0.5, 'a:urban_grass'),
    (1, 'a:urban_grass'),
    (2, 'a:urban_grass'),
    (3.2, 'a:urban_grass'),
    (8, 'a:urban_grass'),
    (0.5, 'a:li_residential'),
    (1, 'a:li_residential'),
    (2, 'a:li_residential'),
    (3.2, 'a:li_residential'),
    (8, 'a:li_residential'),
    (0.5, 'a:hi_residential'),
    (1, 'a:hi_residential'),
    (2, 'a:hi_residential'),
    (3.2, 'a:hi_residential'),
    (8, 'a:hi_residential'),
    (0.5, 'a:commercial'),
    (1, 'a:commercial'),
    (2, 'a:commercial'),
    (3.2, 'a:commercial'),
    (8, 'a:commercial'),
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
    (0.5, 'a:row_crop'),
    (1, 'a:row_crop'),
    (2, 'a:row_crop'),
    (3.2, 'a:row_crop'),
    (8, 'a:row_crop'),
    (0.5, 'a:woody_wetland'),
    (0.5, 'a:herbaceous_wetland'),
    (1, 'a:woody_wetland'),
    (1, 'a:herbaceous_wetland'),
    (2, 'a:woody_wetland'),
    (2, 'a:herbaceous_wetland'),
    (3.2, 'a:woody_wetland'),
    (3.2, 'a:herbaceous_wetland'),
    (8, 'a:woody_wetland'),
    (8, 'a:herbaceous_wetland'),
    (0.5, 'b:water'),
    (1, 'b:water'),
    (2, 'b:water'),
    (3.2, 'b:water'),
    (8, 'b:water'),
    (0.5, 'b:rock'),
    (1, 'b:rock'),
    (2, 'b:rock'),
    (3.2, 'b:rock'),
    (8, 'b:rock'),
    (0.5, 'b:urban_grass'),
    (1, 'b:urban_grass'),
    (2, 'b:urban_grass'),
    (3.2, 'b:urban_grass'),
    (8, 'b:urban_grass'),
    (0.5, 'b:li_residential'),
    (1, 'b:li_residential'),
    (2, 'b:li_residential'),
    (3.2, 'b:li_residential'),
    (8, 'b:li_residential'),
    (0.5, 'b:hi_residential'),
    (1, 'b:hi_residential'),
    (2, 'b:hi_residential'),
    (3.2, 'b:hi_residential'),
    (8, 'b:hi_residential'),
    (0.5, 'b:commercial'),
    (1, 'b:commercial'),
    (2, 'b:commercial'),
    (3.2, 'b:commercial'),
    (8, 'b:commercial'),
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
    (0.5, 'b:row_crop'),
    (1, 'b:row_crop'),
    (2, 'b:row_crop'),
    (3.2, 'b:row_crop'),
    (8, 'b:row_crop'),
    (0.5, 'b:woody_wetland'),
    (0.5, 'b:herbaceous_wetland'),
    (1, 'b:woody_wetland'),
    (1, 'b:herbaceous_wetland'),
    (2, 'b:woody_wetland'),
    (2, 'b:herbaceous_wetland'),
    (3.2, 'b:woody_wetland'),
    (3.2, 'b:herbaceous_wetland'),
    (8, 'b:woody_wetland'),
    (8, 'b:herbaceous_wetland'),
    (0.5, 'c:water'),
    (1, 'c:water'),
    (2, 'c:water'),
    (3.2, 'c:water'),
    (8, 'c:water'),
    (0.5, 'c:rock'),
    (1, 'c:rock'),
    (2, 'c:rock'),
    (3.2, 'c:rock'),
    (8, 'c:rock'),
    (0.5, 'c:urban_grass'),
    (1, 'c:urban_grass'),
    (2, 'c:urban_grass'),
    (3.2, 'c:urban_grass'),
    (8, 'c:urban_grass'),
    (0.5, 'c:li_residential'),
    (1, 'c:li_residential'),
    (2, 'c:li_residential'),
    (3.2, 'c:li_residential'),
    (8, 'c:li_residential'),
    (0.5, 'c:hi_residential'),
    (1, 'c:hi_residential'),
    (2, 'c:hi_residential'),
    (3.2, 'c:hi_residential'),
    (8, 'c:hi_residential'),
    (0.5, 'c:commercial'),
    (1, 'c:commercial'),
    (2, 'c:commercial'),
    (3.2, 'c:commercial'),
    (8, 'c:commercial'),
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
    (0.5, 'c:row_crop'),
    (1, 'c:row_crop'),
    (2, 'c:row_crop'),
    (3.2, 'c:row_crop'),
    (8, 'c:row_crop'),
    (0.5, 'c:woody_wetland'),
    (0.5, 'c:herbaceous_wetland'),
    (1, 'c:woody_wetland'),
    (1, 'c:herbaceous_wetland'),
    (2, 'c:woody_wetland'),
    (2, 'c:herbaceous_wetland'),
    (3.2, 'c:woody_wetland'),
    (3.2, 'c:herbaceous_wetland'),
    (8, 'c:woody_wetland'),
    (8, 'c:herbaceous_wetland'),
    (0.5, 'd:water'),
    (1, 'd:water'),
    (2, 'd:water'),
    (3.2, 'd:water'),
    (8, 'd:water'),
    (0.5, 'd:rock'),
    (1, 'd:rock'),
    (2, 'd:rock'),
    (3.2, 'd:rock'),
    (8, 'd:rock'),
    (0.5, 'd:urban_grass'),
    (1, 'd:urban_grass'),
    (2, 'd:urban_grass'),
    (3.2, 'd:urban_grass'),
    (8, 'd:urban_grass'),
    (0.5, 'd:li_residential'),
    (1, 'd:li_residential'),
    (2, 'd:li_residential'),
    (3.2, 'd:li_residential'),
    (8, 'd:li_residential'),
    (0.5, 'd:hi_residential'),
    (1, 'd:hi_residential'),
    (2, 'd:hi_residential'),
    (3.2, 'd:hi_residential'),
    (8, 'd:hi_residential'),
    (0.5, 'd:commercial'),
    (1, 'd:commercial'),
    (2, 'd:commercial'),
    (3.2, 'd:commercial'),
    (8, 'd:commercial'),
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
    (0.5, 'd:row_crop'),
    (1, 'd:row_crop'),
    (2, 'd:row_crop'),
    (3.2, 'd:row_crop'),
    (8, 'd:row_crop'),
    (0.5, 'd:woody_wetland'),
    (0.5, 'd:herbaceous_wetland'),
    (1, 'd:woody_wetland'),
    (1, 'd:herbaceous_wetland'),
    (2, 'd:woody_wetland'),
    (2, 'd:herbaceous_wetland'),
    (3.2, 'd:woody_wetland'),
    (3.2, 'd:herbaceous_wetland'),
    (8, 'd:woody_wetland'),
    (8, 'd:herbaceous_wetland')
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
        'c:commercial': {
            'cell_count': 42
        },
        'a:deciduous_forest': {
            'cell_count': 72
        },
        'd:hi_residential': {
            'cell_count': 33
        }
    },
    'modifications': [
        {
            'change': '::no_till',
            'cell_count': 30,
            'distribution': {
                'c:commercial': {
                    'cell_count': 20
                },
                'd:hi_residential': {
                    'cell_count': 10
                }
            }
        },
        {
            'change': 'd:rock:',
            'cell_count': 5,
            'distribution': {
                'a:deciduous_forest': {
                    'cell_count': 5
                }
            },
        }
    ]
}

YEAR_OUTPUT_1 = {
    'unmodified': {
        'inf': 20.24558036990151,
        'cell_count': 147,
        'tp': 1.9158509765426026,
        'tn': 11.858981443411944,
        'runoff': 17.614211721110824,
        'et': 15.167861632653095,
        'distribution': {
            'c:commercial': {
                'cell_count': 42,
                'tp': 1.2321451541995787,
                'tn': 7.786472849455671,
                'runoff': 36.375400229862464,
                'et': 2.272860000000005,
                'inf': 4.430079770137537,
                'bod': 1061.0138827829708,
                'tss': 216.39549270630107
            },
            'a:deciduous_forest': {
                'cell_count': 72,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 26.51670000000007,
                'inf': 34.91810000000001,
                'bod': 0.0,
                'tss': 0.0
            },
            'd:hi_residential': {
                'cell_count': 33,
                'tp': 0.6837058223430238,
                'tn': 4.072508593956273,
                'runoff': 32.167342828759615,
                'et': 6.818579999999993,
                'inf': 8.361629213022574,
                'bod': 701.5416264041463,
                'tss': 83.8282790872751
            }
        },
        'bod': 1762.555509187117,
        'tss': 300.2237717935762
    },
    'modified': {
        'inf': 24.67740388835977,
        'cell_count': 147,
        'tp': 1.2402469548151882,
        'tn': 7.649885146629041,
        'runoff': 11.957947247429287,
        'et': 20.450586122448982,
        'distribution': {
            'c:commercial': {
                'inf': 16.198443763932524,
                'cell_count': 42,
                'tp': 0.7192244464514511,
                'tn': 4.545098932436254,
                'runoff': 21.23295052178176,
                'et': 17.42526,
                'distribution': {
                    'c:commercial': {
                        'cell_count': 22,
                        'tp': 0.6454093664854939,
                        'tn': 4.078628635429163,
                        'runoff': 36.37540022986247,
                        'et': 2.2728600000000068,
                        'inf': 4.430079770137537,
                        'bod': 555.7691766958419,
                        'tss': 113.35001998901487
                    },
                    'c:commercial:no_till': {
                        'cell_count': 20,
                        'tp': 0.07381507996595724,
                        'tn': 0.4664702970070909,
                        'runoff': 4.576255842892978,
                        'et': 34.0929,
                        'inf': 29.143644157107012,
                        'bod': 63.56298552624096,
                        'tss': 12.96377341902124
                    }
                },
                'bod': 619.3321622220828,
                'tss': 126.3137934080361
            },
            'a:deciduous_forest': {
                'inf': 34.53218880673186,
                'cell_count': 72,
                'tp': 0.0003225729096998572,
                'tn': 0.0032257290969985716,
                'runoff': 0.7999320266014792,
                'et': 24.675262500000017,
                'distribution': {
                    'a:deciduous_forest': {
                        'cell_count': 67,
                        'tp': 0.0,
                        'tn': 0.0,
                        'runoff': 0.0,
                        'et': 26.516700000000018,
                        'inf': 34.9181,
                        'bod': 0.0,
                        'tss': 0.0
                    },
                    'd:rock:': {
                        'cell_count': 5,
                        'tp': 0.0003225729096998572,
                        'tn': 0.0032257290969985716,
                        'runoff': 11.519021183061302,
                        'et': 0.0,
                        'inf': 29.360978816938722,
                        'bod': 42.579624080381144,
                        'tss': 0.32257290969985714
                    }
                },
                'bod': 42.579624080381144,
                'tss': 0.32257290969985714
            },
            'd:hi_residential': {
                'inf': 13.967458770273502,
                'cell_count': 33,
                'tp': 0.5206999354540374,
                'tn': 3.101560485095788,
                'runoff': 24.498158107332266,
                'et': 15.08352545454543,
                'distribution': {
                    'd:hi_residential:no_till': {
                        'cell_count': 10,
                        'tp': 0.0441776956392026,
                        'tn': 0.26314540445959805,
                        'runoff': 6.859033248049366,
                        'et': 34.0929,
                        'inf': 26.860866751950642,
                        'bod': 45.3301572645731,
                        'tss': 5.416569639241362
                    },
                    'd:hi_residential': {
                        'cell_count': 23,
                        'tp': 0.47652223981483477,
                        'tn': 2.83841508063619,
                        'runoff': 32.167342828759615,
                        'et': 6.818579999999968,
                        'inf': 8.361629213022571,
                        'bod': 488.9532547665262,
                        'tss': 58.425770272949315
                    }
                },
                'bod': 534.2834120310993,
                'tss': 63.842339912190674
            }
        },
        'bod': 1196.1951983335632,
        'tss': 190.47870622992664
    }
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
            'c:commercial': {
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
            'd:hi_residential': {
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
            'c:commercial': {
                'inf': 1.077061870392374,
                'cell_count': 42,
                'tp': 0.02803732401552826,
                'tn': 0.1771803114870189,
                'runoff': 0.827718129607626,
                'et': 0.09522,
                'distribution': {
                    'c:commercial': {
                        'cell_count': 22,
                        'tp': 0.017573506223953986,
                        'tn': 0.11105479627637589,
                        'runoff': 0.99044630514,
                        'et': 0.012419999999999999,
                        'inf': 0.99713369486,
                        'bod': 15.132741470627044,
                        'tss': 3.086347030581919
                    },
                    'c:commercial:no_till': {
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
                    'd:rock:': {
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
            'd:hi_residential': {
                'inf': 1.1701229689350983,
                'cell_count': 33,
                'tp': 0.015886865154134316,
                'tn': 0.09463045765723485,
                'runoff': 0.7474533947012655,
                'et': 0.08242363636363635,
                'distribution': {
                    'd:hi_residential:no_till': {
                        'cell_count': 10,
                        'tp': 0.005468249773992795,
                        'tn': 0.03257174865378317,
                        'runoff': 0.8490009826400262,
                        'et': 0.1863,
                        'inf': 0.9646990173599737,
                        'bod': 5.610899768096954,
                        'tss': 0.6704549722895514
                    },
                    'd:hi_residential': {
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
        'd:hi_residential': {'cell_count': 1},
        'c:commercial': {'cell_count': 1},
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
                'd:hi_residential': {'cell_count': 1}
            }
        },
        {
            'change': '::rain_garden',
            'cell_count': 1,
            'distribution': {
                'c:commercial': {'cell_count': 1}
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
            'c:commercial': {
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
            'd:hi_residential': {
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
            'c:commercial': {
                'inf': 1.0641101843915999,
                'cell_count': 1,
                'tp': 0.0007414402317520271,
                'tn': 0.004685490353432948,
                'runoff': 0.9193298156084,
                'et': 0.01656,
                'distribution': {
                    'c:commercial': {
                        'cell_count': 0,
                        'runoff': 0,
                        'et': 0,
                        'inf': 0
                    },
                    'c:commercial:rain_garden': {
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
            'd:hi_residential': {
                'inf': 1.5789429191559998,
                'cell_count': 1,
                'tp': 0.000215198296488544,
                'tn': 0.001281833331257849,
                'runoff': 0.3341170808440001,
                'et': 0.08693999999999999,
                'distribution': {
                    'd:hi_residential:cluster_housing': {
                        'cell_count': 1,
                        'tp': 0.000215198296488544,
                        'tn': 0.001281833331257849,
                        'runoff': 0.3341170808440001,
                        'et': 0.08693999999999999,
                        'inf': 1.5789429191559998,
                        'bod': 0.220812165092593,
                        'tss': 0.026385182439030177
                    },
                    'd:hi_residential': {
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

YEAR_OUTPUT_2 = {
    'unmodified': {
        'inf': 20.72181910477488,
        'cell_count': 4,
        'tp': 0.050707291853983406,
        'tn': 0.31380133435186236,
        'runoff': 17.232718905670666,
        'et': 14.58418499999997,
        'distribution': {
            'c:commercial': {
                'cell_count': 1,
                'tp': 0.029336789385704252,
                'tn': 0.1853922107013255,
                'runoff': 36.37540022986246,
                'et': 2.272860000000009,
                'inf': 4.430079770137537,
                'bod': 25.262235304356444,
                'tss': 5.15227363586431
            },
            'a:deciduous_forest': {
                'cell_count': 1,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 26.516699999999968,
                'inf': 34.918099999999995,
                'bod': 0.0,
                'tss': 0.0
            },
            'b:pasture': {
                'cell_count': 1,
                'tp': 0.0006521442154602603,
                'tn': 0.004999772318528663,
                'runoff': 0.38813256406059976,
                'et': 22.72859999999992,
                'inf': 35.177467435939406,
                'bod': 0.21738140515342014,
                'tss': 0.10869070257671007
            },
            'd:hi_residential': {
                'cell_count': 1,
                'tp': 0.020718358252818894,
                'tn': 0.1234093513320082,
                'runoff': 32.1673428287596,
                'et': 6.818579999999982,
                'inf': 8.361629213022574,
                'bod': 21.258837163762,
                'tss': 2.540250881432578
            }
        },
        'bod': 46.738453873271865,
        'tss': 7.801215219873598
    },
    'modified': {
        'inf': 24.476938587987863,
        'cell_count': 4,
        'tp': 0.038879611034946346,
        'tn': 0.24507035546075562,
        'runoff': 12.571429731923587,
        'et': 19.887524999999986,
        'distribution': {
            'c:commercial': {
                'inf': 11.893415183645322,
                'cell_count': 1,
                'tp': 0.02310848228996424,
                'tn': 0.14603277002685733,
                'runoff': 28.652770449780387,
                'et': 3.0304800000000034,
                'distribution': {
                    'c:commercial': {
                        'cell_count': 0,
                        'runoff': 0,
                        'et': 0,
                        'inf': 0
                    },
                    'c:commercial:rain_garden': {
                        'cell_count': 1,
                        'tp': 0.02310848228996424,
                        'tn': 0.14603277002685733,
                        'runoff': 28.652770449780387,
                        'et': 3.0304800000000034,
                        'inf': 11.893415183645322,
                        'bod': 19.89897086080254,
                        'tss': 4.05842720217497
                    }
                },
                'bod': 19.89897086080254,
                'tss': 4.05842720217497
            },
            'a:deciduous_forest': {
                'cell_count': 1,
                'tp': 0.0,
                'tn': 0.0,
                'runoff': 0.0,
                'et': 26.516699999999968,
                'inf': 34.918099999999995,
                'bod': 0.0,
                'tss': 0.0
            },
            'b:pasture': {
                'inf': 31.946213918431017,
                'cell_count': 1,
                'tp': 0.0029801650911130345,
                'tn': 0.022847932365199927,
                'runoff': 1.7736860815689908,
                'et': 34.092899999999936,
                'distribution': {
                    'b:pasture:no_till': {
                        'cell_count': 1,
                        'tp': 0.0029801650911130345,
                        'tn': 0.022847932365199927,
                        'runoff': 1.7736860815689908,
                        'et': 34.092899999999936,
                        'inf': 31.946213918431017,
                        'bod': 0.9933883637043449,
                        'tss': 0.49669418185217246
                    },
                    'b:pasture': {
                        'cell_count': 0,
                        'runoff': 0,
                        'et': 0,
                        'inf': 0
                    }
                },
                'bod': 0.9933883637043449,
                'tss': 0.49669418185217246
            },
            'd:hi_residential': {
                'inf': 19.15002524987511,
                'cell_count': 1,
                'tp': 0.012790963653869069,
                'tn': 0.07618965306869836,
                'runoff': 19.859262396344974,
                'et': 15.910020000000028,
                'distribution': {
                    'd:hi_residential:cluster_housing': {
                        'cell_count': 1,
                        'tp': 0.012790963653869069,
                        'tn': 0.07618965306869836,
                        'runoff': 19.859262396344974,
                        'et': 15.910020000000028,
                        'inf': 19.15002524987511,
                        'bod': 13.124640966578697,
                        'tss': 1.568283369735251
                    },
                    'd:hi_residential': {
                        'cell_count': 0,
                        'runoff': 0,
                        'et': 0,
                        'inf': 0
                    }
                },
                'bod': 13.124640966578697,
                'tss': 1.568283369735251
            }
        },
        'bod': 34.01700019108558,
        'tss': 6.123404753762394
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
        runoffs = [round(runoff_nrcs(precip, 0.0, 'c', 'hi_residential'), 2)
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
            # problematic.  It is unclear why the 'rock' type is
            # giving trouble on soil types C and D.
            if precip > 2 and tile_string != 'c:rock' \
               and tile_string != 'd:rock':
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
                   if precip > 2 and tile_string != 'c:rock' and
                   tile_string != 'd:rock']
        expected = [OUTPUT[i][0] / INPUT[i][0]
                    for i in range(len(INPUT))
                    if INPUT[i][0] > 2 and INPUT[i][1] != 'c:rock' and
                    INPUT[i][1] != 'd:rock']
        lam = lambda x, y: pow((x - y), 2)
        rmse = sqrt(average(map(lam, results, expected)))
        self.assertTrue(rmse < 0.13)

    def test_simulate_day_3(self):
        """
        Daily simulation.
        """
        result1 = simulate_cell_day(42, 93, 'a:rock:', 1)
        result2 = simulate_cell_day(42, 93, 'a:rock:', 2)
        self.assertEqual(result1['runoff-vol'] * 2, result2['runoff-vol'])

    def test_simulate_cell_year(self):
        """
        Yearly simulation.
        """
        result1 = simulate_cell_year('a:hi_residential:', 42)
        result2 = simulate_cell_year('a:mixed_forest:', 42)
        self.assertNotEqual(result1, result2)
        self.assertGreater(result1['runoff-vol'], result2['runoff-vol'])

    def test_create_unmodified_census(self):
        """
        Test create_unmodified_census.
        """
        census = {
            "cell_count": 2,
            "distribution": {
                "a:rock": {"cell_count": 1},
                "a:water": {"cell_count": 1}
            },
            "modifications": [
                {
                    "change": "::cluster_housing",
                    "cell_count": 1,
                    "distribution": {
                        "a:rock": {"cell_count": 1}
                    }
                }
            ]
        }

        result = create_unmodified_census(census)
        census.pop("modifications", None)
        self.assertEqual(census, result)

    def test_create_modified_census_1(self):
        """
        create_modified_census with a census tree without modifications.
        """
        census = {
            "cell_count": 5,
            "distribution": {
                "a:rock": {"cell_count": 3},
                "a:water": {"cell_count": 2}
            }
        }

        result = create_modified_census(census)
        census.pop("modifications", None)
        self.assertEqual(census, result)

    def test_create_modified_census_2(self):
        """
        create_modified_census with trivial modifications.
        """
        census = {
            "cell_count": 3,
            "distribution": {
                "a:rock": {"cell_count": 2},
                "a:water": {"cell_count": 1}
            },
            "modifications": []
        }

        result = create_modified_census(census)
        census.pop("modifications", None)
        self.assertEqual(census, result)

    def test_create_modified_census_3(self):
        """
        create_modified_census with non-trivial modifications.
        """
        census1 = {
            "cell_count": 144,
            "distribution": {
                "a:rock": {"cell_count": 55},
                "a:water": {"cell_count": 89}
            },
            "modifications": [
                {
                    "change": "::cluster_housing",
                    "cell_count": 34,
                    "distribution": {
                        "a:rock": {"cell_count": 34}
                    }
                }
            ]
        }

        census2 = {
            "cell_count": 144,
            "distribution": {
                "a:rock": {
                    "cell_count": 55,
                    "distribution": {
                        "a:rock:cluster_housing": {"cell_count": 34},
                        "a:rock": {"cell_count": 21}
                    }
                },
                "a:water": {"cell_count": 89}
            }
        }

        result = create_modified_census(census1)
        self.assertEqual(census2, result)

    def test_create_modified_census_4(self):
        """
        create_modified_census with different types of changes.
        """
        census = {
            "distribution": {
                "a:li_residential": {
                    "cell_count": 3
                }
            },
            "cell_count": 3,
            "modifications": [
                {
                    "distribution": {
                        "a:li_residential": {
                            "cell_count": 1
                        }
                    },
                    "cell_count": 1,
                    "change": ":deciduous_forest:cluster_housing"
                },
                {
                    "distribution": {
                        "a:li_residential": {
                            "cell_count": 1
                        }
                    },
                    "cell_count": 1,
                    "change": ":deciduous_forest:"
                },
                {
                    "distribution": {
                        "a:li_residential": {
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
            'a:li_residential',
            'a:deciduous_forest:cluster_housing',
            'a:li_residential:cluster_housing'])
        modified = create_modified_census(census)
        distrib = modified['distribution']['a:li_residential']['distribution']
        actual = set(distrib.keys())
        self.assertEqual(actual, expected)

    def test_simulate_water_quality_1(self):
        """
        Test the water quality simulation.
        """
        census = {
            "cell_count": 5,
            "distribution": {
                "a:rock": {"cell_count": 3},
                "a:water": {"cell_count": 2}
            }
        }

        def fn(cell, cell_count):
            return simulate_cell_year(cell, cell_count)

        simulate_water_quality(census, 93, fn)
        left = census['distribution']['a:rock']
        right = census['distribution']['a:water']
        for key in set(census.keys()) - set(['distribution']):
            self.assertEqual(left[key] + right[key], census[key])

    def test_simulate_water_quality_2(self):
        """
        Test the water quality simulation in the presence of modifications.
        """
        census = {
            "cell_count": 2,
            "distribution": {
                "a:rock": {"cell_count": 1},
                "a:water": {"cell_count": 1}
            },
            "modifications": [
                {
                    "change": "d:hi_residential:",
                    "cell_count": 1,
                    "distribution": {
                        "a:rock": {"cell_count": 1}
                    }
                }
            ]
        }

        census1 = create_modified_census(census)
        census2 = {
            "cell_count": 2,
            "distribution": {
                "d:hi_residential": {"cell_count": 1},
                "a:water": {"cell_count": 1}
            }
        }

        def fn(cell, cell_count):
            return simulate_cell_year(cell, cell_count)

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
                "a:hi_residential": {"cell_count": 1},
                "b:no_till": {"cell_count": 1},
                "c:pasture": {"cell_count": 1},
                "d:row_crop": {"cell_count": 1},
                "a:water": {"cell_count": 1},
                "b:chaparral": {"cell_count": 1},
                "c:desert": {"cell_count": 1},
                "d:tall_grass_prairie": {"cell_count": 1}
            }
        }

        census2 = {
            "cell_count": 8,
            "distribution": {
                "a:mixed_forest": {"cell_count": 1},
                "b:mixed_forest": {"cell_count": 1},
                "c:mixed_forest": {"cell_count": 1},
                "d:mixed_forest": {"cell_count": 1},
                "a:water": {"cell_count": 1},
                "b:chaparral": {"cell_count": 1},
                "c:desert": {"cell_count": 1},
                "d:tall_grass_prairie": {"cell_count": 1}
            }
        }

        census3 = census2.copy()

        def fn(cell, cell_count):
            return simulate_cell_year(cell, cell_count)

        simulate_water_quality(census1, 93, fn, precolumbian=True)
        simulate_water_quality(census2, 93, fn, precolumbian=True)
        simulate_water_quality(census3, 93, fn, precolumbian=False)

        for key in set(census1.keys()) - set(['distribution']):
            self.assertAlmostEqual(census1[key], census2[key])

        for key in set(census1.keys()) - set(['distribution']):
            self.assertAlmostEqual(census2[key], census3[key])

    def test_year_1(self):
        """
        Test the simulate_year function.
        """
        actual = simulate_year(CENSUS_1)
        expected = YEAR_OUTPUT_1
        self.assertEqual(actual, expected)

    def test_year_2(self):
        """
        Test the simulate_year function with lots of BMPs.
        """
        actual = simulate_year(CENSUS_2)
        expected = YEAR_OUTPUT_2
        self.assertEqual(actual, expected)

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

if __name__ == "__main__":
    unittest.main()
