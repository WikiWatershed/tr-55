"""
Various routines to do table lookups.
"""

from datetime import date
from tr55.tables import *

def lookupET(simulationDay, landUse):
    """
    Lookup/compute evapotranspiration from the tables.
    """
    fixedYear = SampleYear['yearStart'].year
    simulationDay = date(fixedYear, simulationDay.month, simulationDay.day)

    # Compute $ET_{\max}$ based on the time of year
    if (SampleYear['growingStart'] <= simulationDay) and (simulationDay <= SampleYear['growingEnd']):
        ETmax = SampleYear['growingETmax']
    else:
        ETmax = SampleYear['nonGrowingETmax']

    # Compute the landuse coefficient
    try:
        Ki = TableA[landUse]
    except:
        raise Exception('Unknown Land Use')

    # Report $ET$, the evapotranspiration
    return ETmax * Ki

def lookupP(simulationDay):
    """
    Lookup percipitation from the SampleYear table.
    """
    arbitraryYear = SampleYear['yearStart'].year
    simulationDay = date(arbitraryYear, simulationDay.month, simulationDay.day)
    secondsPerDay = 60 * 60 * 24
    daysPerYear = SampleYear['daysPerYear']
    daysFromStart = (int)((simulationDay - SampleYear['yearStart']).total_seconds() / secondsPerDay)

    days = (daysFromStart + daysPerYear) % daysPerYear
    for consecutiveDays, P in SampleYear['precipitation']:
        if 0 <= days and days < consecutiveDays:
            return P
        days -= consecutiveDays
    raise Exception('No Data for Day')

def lookupBMPInfiltration(soilType, BMP):
    """
    Lookup the amount of infiltration causes by a particular BMP.
    """
    try:
        return TableB[soilType][BMP]
    except:
        raise Exception('Not a BMP and/or BMP Incompatible with Soil Type')

def lookupCN(soilType, landUse):
    """
    Lookup the runoff curve number for a particular soil type and land use.
    """
    try:
        return TableC[soilType][landUse]
    except:
        raise Exception('Unknown Soil Type and/or Land Use')

def isBMP(landUse):
    """
    Test to see if the land use is a BMP.
    """
    return landUse in BMPs

def isBuiltType(landUse):
    """
    Test to see if the land use is a "built type".
    """
    return landUse in BuiltTypes
