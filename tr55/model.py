"""
TR-55 Model Implementation

A mapping between variable/parameter names found in the TR-55 document
and variables used in this program are as follows:
 * `precip` is referred to as P in the report
 * `runoff` is Q
 * `evaptrans` maps to ET, the evapotranspiration
 * `inf` is the amount of water that infiltrates into the soil (in inches)
 * `init_abs` is Ia, the initial abstraction, another form of infiltration
"""

from datetime import date, timedelta
from tr55.tablelookup import days_in_sample_year
from tr55.tablelookup import lookup_et, lookup_p, lookup_cn
from tr55.tablelookup import lookup_bmp_infiltration, is_bmp, is_built_type


def runoff_pitt(precip, land_use):
    """
    The Pitt Small Storm Hydrology method.  This comes from Table D in
    the 2010/12/27 document.  The output is a runoff value in inches.
    """
    co1 = +3.638858398e-2
    co2 = -1.243464039e-1
    co3 = +1.295682223e-1
    co4 = +9.375868043e-1
    co5 = -2.235170859e-2
    co6 = +0.170228067e0
    co7 = -3.971810782e-1
    co8 = +3.887275538e-1
    co9 = -2.289321859e-2
    pr4 = pow(precip, 4)
    pr3 = pow(precip, 3)
    pr2 = pow(precip, 2)

    impervious = (co1 * pr3) + (co2 * pr2) + (co3 * precip) + co4
    urb_grass = (co5 * pr4) + (co6 * pr3) + (co7 * pr2) + (co8 * precip) + co9

    runoff_vals = {
        'water':          impervious,
        'li_residential': 0.20 * impervious + 0.80 * urb_grass,
        'cluster_housing': 0.20 * impervious + 0.80 * urb_grass,
        'hi_residential': 0.65 * impervious + 0.35 * urb_grass,
        'commercial':     impervious,
        'industrial':     impervious,
        'transportation': impervious,
        'urban_grass':     urb_grass
    }
    if land_use not in runoff_vals:
        raise Exception('Land use %s not a built-type' % land_use)
    else:
        return min(runoff_vals[land_use], precip)


def nrcs_cutoff(precip, curve_number):
    """
    A function to find the cutoff between preciptation/curve number
    pairs that have zero runoff by definition, and those that do not.
    """
    if precip <= -1 * (2 * (curve_number - 100.0) / curve_number):
        return True
    else:
        return False


def runoff_nrcs(precip, evaptrans, soil_type, land_use):
    """
    The runoff equation from the TR-55 document.  The output is a
    runoff value in inches.
    """
    curve_number = lookup_cn(soil_type, land_use)
    if nrcs_cutoff(precip, curve_number):
        return 0
    potential_retention = (1000.0 / curve_number) - 10
    initial_abs = 0.2 * potential_retention
    precip_minus_initial_abs = precip - initial_abs
    numerator = pow(precip_minus_initial_abs, 2)
    denominator = (precip_minus_initial_abs + potential_retention)
    runoff = numerator / denominator
    return min(runoff, precip - evaptrans)


def simulate_tile(parameters, tile_string, pre_columbian=False):
    """
    Simulate a tile on a given day using the method given in the
    flowchart 2011_06_16_Stroud_model_diagram_revised.PNG and as
    revised by various emails.

    The first argument can be one of two types.  It can either be a
    date object, in which case the precipitation and
    evapotranspiration are looked up from the sample year table.
    Alternatively, those two values can be supplied directly via this
    argument as a tuple.

    The second argument is a string which contains a soil type and
    land use separted by a colon.

    The third argument is a boolean which is true if pre-Columbian
    circumstances are to be simulated and false otherwise.

    The return value is a triple of runoff, evapotranspiration, and
    infiltration.
    """
    tile_string = tile_string.lower();
    soil_type, land_use = tile_string.split(':')

    pre_columbian_land_uses = set([
        'water',
        'woody_wetland',
        'herbaceous_wetland'
    ])

    if pre_columbian:
        if land_use not in pre_columbian_land_uses:
            land_use = 'mixed_forest'

    if type(parameters) is date:
        precip = lookup_p(parameters)  # precipitation
        evaptrans = lookup_et(parameters, land_use)  # evapotranspiration
    elif type(parameters) is tuple:
        precip, evaptrans = parameters
    else:
        raise Exception('First argument must be a date or a (P,ET) pair')

    if precip == 0.0:
        return (0.0, evaptrans, 0.0)

    if is_bmp(land_use) and land_use != 'rain_garden':
        inf = lookup_bmp_infiltration(soil_type, land_use)  # infiltration
        runoff = precip - (evaptrans + inf)  # runoff
        return (runoff, evaptrans, inf)  # Q, ET, Inf.
    elif land_use == 'rain_garden':
        # Here, return a mixture of 20% ideal rain garden and 80% high
        # intensity residential.
        inf = lookup_bmp_infiltration(soil_type, land_use)
        runoff = precip - (evaptrans + inf)
        hi_res_tile = soil_type + ':hi_residential'
        hi_res = simulate_tile((precip, evaptrans), hi_res_tile)
        return (0.2 * runoff + 0.8 * hi_res[0],
                0.2 * evaptrans + 0.8 * hi_res[1],
                0.2 * inf + 0.8 * hi_res[2])

    if is_built_type(land_use) and precip <= 2.0:
        runoff = runoff_pitt(precip, land_use)
    elif is_built_type(land_use):
        pitt_runoff = runoff_pitt(2.0, land_use)
        nrcs_runoff = runoff_nrcs(precip, evaptrans, soil_type, land_use)
        runoff = max(pitt_runoff, nrcs_runoff)
    else:
        runoff = runoff_nrcs(precip, evaptrans, soil_type, land_use)
    inf = precip - (evaptrans + runoff)
    return (runoff, evaptrans, max(inf, 0.0))


def simulate_all_tiles(parameters, tile_census, pre_columbian=False):
    """
    Simulate each tile for one day and return the overall results.

    The first argument is either a day or a P,ET double (as in simulate_tile).

    The second argument is a dictionary (presumably converted from
    JSON) that gives the number of each type of tile in the query
    polygon.

    The output is a runoff, evapotranspiration, infiltration triple
    which is an average of those produced by all of the tiles.
    """
    if 'result' not in tile_census:
        raise Exception('No "result" key')
    elif 'cell_count' not in tile_census['result']:
        raise Exception('No "result.cell_count" key')
    elif 'distribution' not in tile_census['result']:
        raise Exception('No "result.distribution" key')

    global_count = tile_census['result']['cell_count']

    def simulate(tile_string, local_count):
        """
        A local helper function which captures various values.
        """
        return [(x * local_count) / global_count
                for x in simulate_tile(parameters, tile_string, pre_columbian)]

    results = [simulate(tile, n)
               for tile, n in tile_census['result']['distribution'].items()]
    return reduce(lambda (a, b, c), (x, y, z): (a+x, b+y, c+z),
                  results,
                  (0.0, 0.0, 0.0))


def simulate_year(tile_census, pre_columbian=False):
    """
    Simulate an entire year.
    """
    year = [date(1, 1, 1) + timedelta(days=i)
            for i in range(days_in_sample_year())]
    simulated_year = [simulate_all_tiles(day, tile_census, pre_columbian)
                      for day in year]

    def day_add(one, two):
        """
        Add two simulated days.
        """
        (runoff1, et1, inf1) = one
        (runoff2, et2, inf2) = two
        return (runoff1 + runoff2, et1 + et2, inf1 + inf2)

    return reduce(day_add, simulated_year)
