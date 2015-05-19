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
    create_unmodified_census, create_modified_census
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


def simulate(precip, tile_string):
    soil_type, land_use = tile_string.split(':')
    ki = lookup_ki(land_use)
    return simulate_cell_day((precip, 0.207 * ki), tile_string, 1)


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
        # quantities, relative to precipitation, compared to the
        # sample output that was emailed to us.
        def similar(incoming, expected):
            precip, tile_string = incoming
            results = simulate(precip, tile_string)
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
        results = [simulate(precip, tile_string)['runoff-vol'] / precip
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
        result1 = simulate_cell_day((42, 93), 'a:rock', 1)
        result2 = simulate_cell_day((42, 93), 'a:rock', 2)
        self.assertEqual(result1['runoff-vol'] * 2, result2['runoff-vol'])

    def test_simulate_year(self):
        """
        Yearly simulation.
        """
        result1 = simulate_cell_year('a:hi_residential', 42, False)
        result2 = simulate_cell_year('a:mixed_forest', 42, False)
        self.assertNotEqual(result1, result2)
        self.assertGreater(result1['runoff-vol'], result2['runoff-vol'])

    def test_simulate_year_precolumbian(self):
        """
        Yearly simulation in Pre-Columbian times.
        """
        result1 = simulate_cell_year('a:hi_residential', 42, True)
        result2 = simulate_cell_year('a:mixed_forest', 42, True)
        self.assertEqual(result1, result2)

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
                    "bmp": "cluster_housing",
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
        create_modified_census with a census tree with trivial
        modifications.
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
        create_modified_census with a census tree non-trivial
        modifications.
        """
        census1 = {
            "cell_count": 144,
            "distribution": {
                "a:rock": {"cell_count": 55},
                "a:water": {"cell_count": 89}
            },
            "modifications": [
                {
                    "bmp": "cluster_housing",
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
                        "a:cluster_housing": {"cell_count": 34},
                        "a:rock": {"cell_count": 21}
                    }
                },
                "a:water": {"cell_count": 89}
            }
        }

        result = create_modified_census(census1)
        self.assertEqual(census2, result)

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
            return simulate_cell_year(cell, cell_count, False)

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
                    "reclassification": "d:hi_residential",
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
            return simulate_cell_year(cell, cell_count, False)

        simulate_water_quality(census1, 93, fn)
        simulate_water_quality(census2, 93, fn)
        for key in set(census1.keys()) - set(['distribution']):
            self.assertEqual(census1[key], census2[key])

    def test_simulate_water_quality_precolumbian(self):
        """
        Test the water quality simulation in Pre-Columbian times.
        """
        census1 = {
            "cell_count": 3,
            "distribution": {
                "a:rock": {"cell_count": 1},
                "b:herbaceous_wetland": {"cell_count": 1},
                "a:water": {"cell_count": 1}
            }
        }

        census2 = {
            "cell_count": 3,
            "distribution": {
                "a:mixed_forest": {"cell_count": 1},
                "b:herbaceous_wetland": {"cell_count": 1},
                "a:water": {"cell_count": 1}
            }
        }

        def fn(cell, cell_count):
            return simulate_cell_year(cell, cell_count, True)

        simulate_water_quality(census1, 93, fn)
        simulate_water_quality(census2, 93, fn)
        for key in set(census1.keys()) - set(['distribution']):
            self.assertEqual(census1[key], census2[key])

if __name__ == "__main__":
    unittest.main()
