# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

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

import sys

from tr55.tablelookup import lookup_pet, lookup_cn, lookup_bmp_infiltration, \
    is_bmp, is_built_type, precolumbian, get_pollutants
from tr55.water_quality import get_volume_of_runoff, get_pollutant_load
from tr55.operations import dict_minus, dict_plus


def runoff_pitt(precip, land_use):
    """
    The Pitt Small Storm Hydrology method.  The output is a runoff
    value in inches.
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
    p4 = pow(precip, 4)
    p3 = pow(precip, 3)
    p2 = pow(precip, 2)

    impervious = (c1 * p3) + (c2 * p2) + (c3 * precip) + c4
    urb_grass = (c5 * p4) + (c6 * p3) + (c7 * p2) + (c8 * precip) + c9

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
        raise Exception('Land use %s not a built-type.' % land_use)
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
        return 0.0
    potential_retention = (1000.0 / curve_number) - 10
    initial_abs = 0.2 * potential_retention
    precip_minus_initial_abs = precip - initial_abs
    numerator = pow(precip_minus_initial_abs, 2)
    denominator = (precip_minus_initial_abs + potential_retention)
    runoff = numerator / denominator
    return min(runoff, precip - evaptrans)


def simulate_tile(parameters, tile_string):
    """
    Simulate a single tile with some particular precipitation and
    evapotranspiration.

    The first argument contains the precipitation and
    evapotranspiration as a tuple.

    The second argument is a string which contains a soil type and
    land use separated by a colon.

    The return value is a dictionary of runoff, evapotranspiration, and
    infiltration.
    """
    if type(parameters) is tuple:
        precip, evaptrans = parameters
    else:
        raise Exception('First argument must be a (P,ET) pair')

    tile_string = tile_string.lower()
    soil_type, land_use = tile_string.split(':')

    if precip == 0.0:
        return {
            'runoff': 0.0,
            'et': evaptrans,
            'inf': 0.0,
        }

    if is_bmp(land_use) and land_use != 'rain_garden':
        inf = lookup_bmp_infiltration(soil_type, land_use)  # infiltration
        runoff = precip - (evaptrans + inf)  # runoff
        return {
            'runoff': runoff,
            'et': evaptrans,
            'inf': inf,
        }
    elif land_use == 'rain_garden':
        # Here, return a mixture of 20% ideal rain garden and 80% high
        # intensity residential.
        inf = lookup_bmp_infiltration(soil_type, land_use)
        runoff = precip - (evaptrans + inf)
        hi_res_tile = soil_type + ':hi_residential'
        hi_res = simulate_tile((precip, evaptrans), hi_res_tile)
        return {
            'runoff': 0.2 * runoff + 0.8 * hi_res[0],
            'et': 0.2 * evaptrans + 0.8 * hi_res[1],
            'inf': 0.2 * inf + 0.8 * hi_res[2],
        }

    if is_built_type(land_use) and precip <= 2.0:
        runoff = runoff_pitt(precip, land_use)
    elif is_built_type(land_use):
        pitt_runoff = runoff_pitt(2.0, land_use)
        nrcs_runoff = runoff_nrcs(precip, evaptrans, soil_type, land_use)
        runoff = max(pitt_runoff, nrcs_runoff)
    else:
        runoff = runoff_nrcs(precip, evaptrans, soil_type, land_use)
    inf = precip - (evaptrans + runoff)

    return {
        'runoff': runoff,
        'et': evaptrans,
        'inf': max(inf, 0.0),
    }


def simulate_day(day, tile_census, subst=None, pre_columbian=False):
    """
    Simulate each tile for one day and return the overall results.

    The first argument is an integer representing the day of the year
    (day == 0 represents October 15th) or a precip, et pair.

    The second argument is a dictionary that gives a census of all of the
    tiles in the query area.

    The third argument is the tile string substitution to be applied
    to each tile.  This is used for simulating BMPs and
    reclassifications.

    The fourth argument is a boolean which is true if pre-Columbian
    circumstances are to be simulated and false otherwise.  When this
    argument is true, all land uses except for water and wetland are
    transformed to mixed forest.

    The output is a runoff, evapotranspiration, infiltration dictionary.
    """
    if 'cell_count' not in tile_census:
        raise Exception('No "cell_count" key.')
    elif 'distribution' not in tile_census:
        raise Exception('No "distribution" key.')

    def simulate(tile, n):
        """
        Return the three values in units of inch-tiles instead of inches.
        Inches are an inconvenient unit to work with.
        """
        (soil_type, land_use) = tile.split(':')

        # If a substitution has been supplied, apply it.
        if sys.version_info.major == 3:
            types = (str)
        else:
            types = (str, unicode)
        if isinstance(subst, types) and subst.find(':') >= 0:
            (subst_soil_type, subst_land_use) = subst.split(':')
            if len(subst_soil_type) > 0:
                soil_type = subst_soil_type
            land_use = subst_land_use

        # If a Pre-Columbian simulation has been requested, change the
        # land use type.
        if pre_columbian:
            land_use = precolumbian(land_use)

        # Retrieve the precipitation and evapotranspiration, then run
        # the simulation.
        if isinstance(day, int):
            parameters = lookup_pet(day, land_use)
        else:
            parameters = day

        retval = simulate_tile(parameters, soil_type + ':' + land_use)
        for key in retval.keys():
            retval[key] *= n
        return retval

    results = {tile: simulate(tile, d['cell_count'])
               for tile, d in tile_census['distribution'].items()}

    return {
        'distribution': results
    }


def simulate_year(tile_census, cell_res=10, subst=None, pre_columbian=False):
    """
    Simulate an entire year, including water quality.

    The first argument is a tile census as described in `simulate_day`.

    The second argument is the tile resolution in meters.

    The third parameter is the tile string substitution to be performed.

    The fourth parameter is as in `simulate_day`.
    """
    # perform a daily simulation for each day of the year
    simulated_year = [simulate_day(day, tile_census, subst, pre_columbian)
                      for day in range(365)]

    # add those simulations together
    year_sum = {}
    for day in simulated_year:
        year_sum = dict_plus(year_sum, day)

    # add the results into the census
    retval = dict_plus(year_sum, tile_census)

    # get the land use after the modification.
    if isinstance(subst, str):
        use_after = subst.split(':')[1]
    else:
        user_after = None  # noqa

    # perform water quality computations
    for (pair, result) in retval['distribution'].items():
        use_before = pair.split(':')[1]
        runoff = result['runoff']
        n = result['cell_count']
        liters = get_volume_of_runoff(runoff / n, n, cell_res)
        for pol in get_pollutants():
            # Try to compute the pollutant load with the land use
            # after the modifications.  If that is impossible (there
            # is no modification, the use is modified to a BMP, et
            # cetera) then use the previous land use.
            try:
                load = get_pollutant_load(use_after, pol, liters)
            except:
                load = get_pollutant_load(use_before, pol, liters)
            result[pol] = load

    return retval


def simulate_modifications(tile_census, cell_res=10, pre_columbian=False):
    """
    Simulate an entire year, including effects of modifications.
    """
    def rescale(result):
        if isinstance(result, dict):
            if 'cell_count' in result:
                n = float(result['cell_count'])
                result['runoff'] /= n
                result['et'] /= n
                result['inf'] /= n
            for (key, val) in result.items():
                rescale(val)

    def tally_subresults(result):
        retval = result.copy()
        total = {}
        for (pair, subresult) in result['distribution'].items():
            total = dict_plus(total, subresult)
        retval.update(total)
        retval.pop('modifications', None)
        rescale(retval)
        return retval

    # compute unmodified results
    orig_result = simulate_year(tile_census, cell_res, None, pre_columbian)

    # Compute the census ex-modifications and the subresults for each
    # of the modifications.
    mod_census = tile_census.copy()
    subresults = []
    if 'modifications' in tile_census:
        for (subst, census) in tile_census['modifications'].items():
            mod_census = dict_minus(mod_census, census)
            subresult = simulate_year(census, cell_res, subst, pre_columbian)
            subresults.append(subresult)

    # Compute the result with modifications taken into account.
    mod_result = simulate_year(mod_census, cell_res, None, pre_columbian)
    for subresult in subresults:
        mod_result = dict_plus(mod_result, subresult)

    return {
        'unmodified': tally_subresults(orig_result),
        'modified': tally_subresults(mod_result)
    }
