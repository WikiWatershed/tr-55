# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""
Various routines to do table lookups.
"""

from tr55.tables import BMPS, BUILT_TYPES, LAND_USE_VALUES, \
    NON_NATURAL, POLLUTANTS, POLLUTION_LOADS


def lookup_ki(land_use):
    """
    Lookup the landuse coefficient.
    """
    if land_use not in LAND_USE_VALUES:
        raise Exception('Unknown land use: %s' % land_use)
    elif 'ki' not in LAND_USE_VALUES[land_use]:
        raise Exception('No ki for land use %s' % land_use)
    else:
        return LAND_USE_VALUES[land_use]['ki']


def lookup_bmp_infiltration(soil_type, bmp):
    """
    Lookup the amount of infiltration caused by a particular BMP.
    """
    if bmp not in LAND_USE_VALUES:
        raise Exception('%s not a BMP' % bmp)
    elif 'infiltration' not in LAND_USE_VALUES[bmp]:
        raise Exception('No infiltration value for BMP %s' % bmp)
    elif soil_type not in LAND_USE_VALUES[bmp]['infiltration']:
        raise Exception('BMP %s incompatible with soil %s' % (bmp, soil_type))
    else:
        return LAND_USE_VALUES[bmp]['infiltration'][soil_type]


def lookup_cn(soil_type, land_use):
    """
    Lookup the runoff curve number for a particular soil type and land use.
    """
    if land_use not in LAND_USE_VALUES:
        raise Exception('Unknown land use: %s' % land_use)
    elif 'cn' not in LAND_USE_VALUES[land_use]:
        raise Exception('No curve numbers for land use %s' % land_use)
    elif soil_type not in LAND_USE_VALUES[land_use]['cn']:
        raise Exception('Unknown soil type: %s' % soil_type)
    else:
        return LAND_USE_VALUES[land_use]['cn'][soil_type]


def is_bmp(land_use):
    """
    Test to see if the land use is a BMP.
    """
    return land_use in BMPS


def is_built_type(land_use):
    """
    Test to see if the land use is a "built type".
    """
    return land_use in BUILT_TYPES


def make_precolumbian(land_use):
    """
    Project the given land use to a Pre-Columbian one.
    """
    if land_use in NON_NATURAL:
        return 'mixed_forest'
    else:
        return land_use


def lookup_load(nlcd_class, pollutant):
    """
    Get the Event Mean Concentration of `pollutant` for land use
    class `nlcd_class`
    """
    if pollutant not in ['tn', 'tp', 'bod', 'tss']:
        raise Exception('Unknown pollutant type: %s' % pollutant)
    elif nlcd_class not in POLLUTION_LOADS:
        raise Exception('Unknown NLCD class: %s' % nlcd_class)
    else:
        return POLLUTION_LOADS[nlcd_class][pollutant]


def lookup_nlcd(land_use):
    """
    Get the NLCD number for a particular human-readable land use.
    """
    if land_use not in LAND_USE_VALUES:
        raise Exception('Unknown land use type: %s' % land_use)
    elif 'nlcd' not in LAND_USE_VALUES[land_use]:
        raise Exception('Land use type %s does not have an NLCD class defined',
                        land_use)
    else:
        return LAND_USE_VALUES[land_use]['nlcd']


def get_pollutants():
    """
    Return the list of pollutants.
    """
    return POLLUTANTS
