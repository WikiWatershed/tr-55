"""
Various routines to do table lookups.
"""

from datetime import date
from tr55.tables import SAMPLE_YEAR, BMPS, BUILT_TYPES
from tr55.tables import TABLE_A, TABLE_B, TABLE_C


def lookup_ki(land_use):
    """
    Lookup the landuse coefficient
    """
    if land_use in TABLE_A:
        return TABLE_A[land_use]
    else:
        raise Exception('Unknown land use: %s' % land_use)


def lookup_et(simulation_day, land_use):
    """
    Lookup/compute evapotranspiration from the tables.
    """
    fixed_year = SAMPLE_YEAR['yearStart'].year
    simulation_day = date(fixed_year, simulation_day.month, simulation_day.day)

    # Compute $ET_{\max}$ based on the time of year
    grow_start = SAMPLE_YEAR['growingStart']
    grow_end = SAMPLE_YEAR['growingEnd']
    grow_et = SAMPLE_YEAR['growingETmax']
    nongrow_et = SAMPLE_YEAR['nonGrowingETmax']
    if grow_start <= simulation_day and simulation_day <= grow_end:
        et_max = grow_et
    else:
        et_max = nongrow_et

    # Compute the landuse coefficient
    landuse_coefficient = TABLE_A[land_use]

    # Report $ET$, the evapotranspiration
    return et_max * landuse_coefficient


def lookup_p(simulation_day):
    """
    Lookup percipitation from the SAMPLE_YEAR table.
    """
    fixed_year = SAMPLE_YEAR['yearStart'].year
    simulation_day = date(fixed_year, simulation_day.month, simulation_day.day)
    seconds_per_day = 60 * 60 * 24
    days_per_year = SAMPLE_YEAR['daysPerYear']
    day_delta = simulation_day - SAMPLE_YEAR['yearStart']
    seconds_from_start = day_delta.total_seconds()
    days_from_start = int(seconds_from_start / seconds_per_day)

    days = (days_from_start + days_per_year) % days_per_year
    # This is a bit unattractive.  If it turns out to be a performance
    # problem (which is unlikely), an interval tree can be used or the
    # SAMPLE_YEAR table itself can be reorganized.
    for consecutive_days, precipitation in SAMPLE_YEAR['precipitation']:
        if 0 <= days and days < consecutive_days:
            return precipitation
        days -= consecutive_days
    raise Exception('No percipitation data for %s' % simulation_day)


def lookup_bmp_infiltration(soil_type, bmp):
    """
    Lookup the amount of infiltration causes by a particular BMP.
    """
    if soil_type not in TABLE_B:
        raise Exception('%s not a BMP' % bmp)
    elif bmp not in TABLE_B[soil_type]:
        raise Exception('BMP %s incompatible with soil %s' % (bmp, soil_type))
    else:
        return TABLE_B[soil_type][bmp]


def lookup_cn(soil_type, land_use):
    """
    Lookup the runoff curve number for a particular soil type and land use.
    """
    if soil_type not in TABLE_C:
        raise Exception('Unknown soil type %s' % soil_type)
    elif land_use not in TABLE_C[soil_type]:
        raise Exception('Unknown land use %s' % land_use)
    else:
        return TABLE_C[soil_type][land_use]


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
