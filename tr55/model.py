"""
TR-55 Model Implementation
"""

from datetime import date
from tr55.tablelookup import *

def runoffPitt(P, landUse):
    """
    The Pitt Small Storm Hydrology method.  This comes directly from
    Table D in the 2010/12/27 document.
    """
    c1 = +3.638858398e-2
    c2 = -1.243464039e-1
    c3 = +1.295682223e-1
    c4 = +9.375868043e-1
    c5 = -2.235170859e-2
    c6 = +0.170228067e0
    c7 = -3.971810782e-1
    c8 = +3.887275538e-1
    c9 = -2.289321859e-2
    impervious = (c1 * pow(P, 3)) + (c2 * pow(P, 2)) + (c3 * P) + c4
    urbanGrass = (c5 * pow(P, 4)) + (c6 * pow(P, 3)) + (c7 * pow(P, 2)) + (c8 * P) + c9
    try:
        Q = {
            'Water':          impervious,
            'LI_Residential': 0.20 * impervious + 0.80 * urbanGrass,
            'HI_Residential': 0.65 * impervious + 0.35 * urbanGrass,
            'Commercial':     impervious,
            'Industrial':     impervious,
            'Transportation': impervious,
            'UrbanGrass':     urbanGrass
        }[landUse]
    except:
        raise Exception('Land Use not a Built-Type')
    return min(Q, P)

def runoffNRCS(P, soilType, landUse):
    """
    The runoff equation from the TR-55 document.
    """
    CN = lookupCN(soilType, landUse)
    S = (1000.0 / CN) - 10
    Ia = 0.2 * S
    PminusIa = P - Ia
    Q = pow(PminusIa, 2) / (PminusIa + S)
    return min(Q, P)

def simulateTile(parameters, tileString, preColumbian=False):
    """
    Simulate a tile on a given day using the method given in the
    flowchart 2011_06_16_Stroud_model_diagram_revised.PNG.
    """
    soilType, landUse = tileString.split(':')
    if preColumbian:
        if landUse == 'Water':
            pass
        elif landUse == 'WoodyWetland':
            pass
        elif landUse == 'HerbaceousWetland':
            pass
        else:
            landUse = 'MixedForest'

    if type(parameters) == type(date.today()):
        P = lookupP(parameters) # precipitation
        ET = lookupET(parameters, landUse) # evapotranspiration
    else:
        P, ET = parameters

    if P == 0.0:
        return (0.0, 0.0, 0.0)

    if isBMP(tileString):
        Inf = lookupBMPInfiltration(soilType, landUse) # infiltration
        Q = P - (ET + Inf) # runoff
        return (max(Q, 0.0), ET, Inf) # Q, ET, Inf.

    if isBuiltType(landUse) and P <= 2.0:
        Q = runoffPitt(P, landUse)
    else:
        Q = runoffNRCS(P, soilType, landUse)
    Inf = P - (ET + Q)
    return (Q, ET, max(Inf, 0.0))

def tileByTileTR55(parameters, tileCensus, preColumbian=False):
    """
    Simulate each tile and return the overall results.
    """
    if ('result' not in tileCensus) or ('error' in tileCensus):
        raise Exception('Problem')

    N = tileCensus['result']['cell_count']

    def simulate(tileString, n):
        return ((x * n) / N for x in simulateTile(parameters, tileString, preColumbian))

    results = (simulate(tile, n) for tile, n in tileCensus['result']['distribution'].items())
    return reduce(lambda (a, b, c), (x, y, z): (a+x, b+y, c+z), results, (0.0, 0.0, 0.0))
