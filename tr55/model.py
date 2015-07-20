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

import copy

from tr55.tablelookup import lookup_pet, lookup_cn, lookup_bmp_infiltration, \
    lookup_ki, is_bmp, is_built_type, make_precolumbian, get_pollutants
from tr55.water_quality import get_volume_of_runoff, get_pollutant_load
from tr55.operations import dict_plus


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
        'water':           impervious,
        'li_residential':  0.20 * impervious + 0.80 * urb_grass,
        'cluster_housing': 0.20 * impervious + 0.80 * urb_grass,
        'hi_residential':  0.65 * impervious + 0.35 * urb_grass,
        'commercial':      impervious,
        'industrial':      impervious,
        'transportation':  impervious,
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
    if land_use == 'cluster_housing':
        land_use = 'li_residential'
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


def simulate_cell_day(precip, evaptrans, cell, cell_count):
    """
    Simulate a bunch of cells of the same type during a one-day event.

    `precip` is the amount of precipitation in inches.

    `evaptrans` is evapotranspiration.

    `cell` is a string which contains a soil type and land use
    separated by a colon.

    `cell_count` is the number of cells to simulate.

    The return value is a dictionary of runoff, evapotranspiration, and
    infiltration as volumes of water.
    """
    soil_type, land_use, bmp = cell.lower().split(':')

    # If there is no precipitation, then there is no runoff or
    # infiltration.  There is evapotranspiration, however (is
    # understood that over a period of time, this can lead to the sum
    # of the three values exceeding the total precipitation).
    if precip == 0.0:
        return {
            'runoff-vol': 0.0,
            'et-vol': cell_count * evaptrans,
            'inf-vol': 0.0
        }

    # Deal with the Best Management Practices (BMPs).  For most BMPs,
    # the infiltration is read from the table and the runoff is what
    # is left over after infiltration and evapotranspiration.  Rain
    # gardens are treated differently.
    if bmp and is_bmp(bmp) and bmp != 'rain_garden':
        inf = lookup_bmp_infiltration(soil_type, bmp)  # infiltration
        runoff = precip - (evaptrans + inf)  # runoff
        return {
            'runoff-vol': cell_count * runoff,
            'et-vol': cell_count * evaptrans,
            'inf-vol': cell_count * inf
        }
    elif bmp and bmp == 'rain_garden':
        # Here, return a mixture of 20% ideal rain garden and 80% high
        # intensity residential.
        inf = lookup_bmp_infiltration(soil_type, bmp)
        runoff = precip - (evaptrans + inf)
        hi_res_cell = soil_type + ':hi_residential:'
        hi_res = simulate_cell_day(precip, evaptrans, hi_res_cell, 1)
        hir_run = hi_res['runoff-vol']
        hir_et = hi_res['et-vol']
        hir_inf = hi_res['inf-vol']
        return {
            'runoff-vol': cell_count * (0.2 * runoff + 0.8 * hir_run),
            'et-vol': cell_count * (0.2 * evaptrans + 0.8 * hir_et),
            'inf-vol': cell_count * (0.2 * inf + 0.8 * hir_inf)
        }

    # At this point, if the `bmp` string has non-zero length, it is
    # equal to either 'no_till' or 'cluster_housing'.
    land_use = bmp or land_use

    # When the land use is a built-type and the level of precipitation
    # is two inches or less, use the Pitt Small Storm Hydrology Model.
    # When the land use is a built-type but the level of precipitation
    # is higher, the runoff is the larger of that predicted by the
    # Pitt model and NRCS model.  Otherwise, return the NRCS amount.
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
        'runoff-vol': cell_count * runoff,
        'et-vol': cell_count * evaptrans,
        'inf-vol': cell_count * max(inf, 0.0),
    }


def simulate_cell_year(cell, cell_count, precolumbian):
    """
    Simulate a cell-type for an entire year using sample precipitation and
    evapotranspiration data.

    The `cell` parameter is a string with the soil type and land use
    separated by a colon.

    The `cell_count` parameter is the number of cells of this type.

    If the `precolumbian` parameter is true, then the cell is
    simulated under Pre-Columbian circumstances (anything other than
    water, woody wetland, and herbaceous wetland becomes mixed
    forest).
    """
    split = cell.split(':')
    if (len(split) == 2):
        split.append('')

    if precolumbian:
        split[1] = make_precolumbian(split[1])

    cell = '%s:%s:%s' % tuple(split[:3])
    land_use = split[1]
    bmp = split[2]

    retval = {}
    for day in range(365):
        (precip, evaptrans) = lookup_pet(day, bmp or land_use)
        result = simulate_cell_day(precip, evaptrans, cell, cell_count)
        retval = dict_plus(retval, result)
    return retval


def create_unmodified_census(census):
    """
    This creates a cell census, ignoring any modifications.  The
    output is suitable for use with `simulate_water_quality`.
    """
    unmod = copy.deepcopy(census)
    unmod.pop('modifications', None)
    return unmod


def create_modified_census(census):
    """
    This creates a cell census, with modifications, that is suitable
    for use with `simulate_water_quality`.

    For every type of cell that undergoes modification, the
    modifications are indicated with a sub-distribution under that
    cell type.
    """
    mod = copy.deepcopy(census)
    mod.pop('modifications', None)

    if 'modifications' in census:
        for modification in census['modifications']:
            for (cell, subcensus) in modification['distribution'].items():
                parent = mod['distribution'][cell]
                n = parent['cell_count']
                m = subcensus['cell_count']

                if 'change' in modification:
                    soil_1, land_1 = cell.split(':')
                    soil_2, land_2, bmp = modification['change'].split(':')
                    soil = soil_2 or soil_1
                    land = land_2 or land_1
                    changed_cell = '%s:%s:%s' % (soil, land, bmp)
                else:
                    raise Exception('Unknown modification type.')

                parent['distribution'] = {
                    cell: {"cell_count": n - m},
                    changed_cell: {"cell_count": m}
                }

    return mod


def simulate_water_quality(tree, cell_res, fn, current_cell=None):
    """
    Perform a water quality simulation by doing simulations on each of
    the cell types (leaves), then adding them together by summing the
    values of a node's subtrees and storing them at that node.

    `tree` is the (sub)tree of cell distributions that is currently
    under consideration.

    `cell_res` is the size of each cell (used for turning inches of
    water into volumes of water).

    `fn` is a function that takes a cell type and a number of cells
    and returns a dictionary containing runoff, et, and inf as
    volumes.

    `current_cell` is the cell type for the present node.
    """
    # Internal node.
    if 'cell_count' in tree and 'distribution' in tree:
        n = tree['cell_count']

        # simulate subtrees
        if n != 0:
            tally = {}
            for cell, subtree in tree['distribution'].items():
                simulate_water_quality(subtree, cell_res, fn, cell)
                subtree_ex_dist = subtree.copy()
                subtree_ex_dist.pop('distribution', None)
                tally = dict_plus(tally, subtree_ex_dist)
                tree.update(tally)  # update this node

        # effectively a leaf
        elif n == 0:
            for pol in get_pollutants():
                tree[pol] = 0.0

    # Leaf node.
    elif 'cell_count' in tree and 'distribution' not in tree:
        n = tree['cell_count']
        result = fn(current_cell, n)  # runoff, et, inf
        tree.update(result)

        # water quality
        if n != 0:
            split = current_cell.split(':')
            if (len(split) == 2):
                split.append('')
            soil_type, land_use, bmp = split
            runoff = result['runoff-vol'] / n
            liters = get_volume_of_runoff(runoff, n, cell_res)
            for pol in get_pollutants():
                tree[pol] = get_pollutant_load(land_use, pol, liters)


def postpass(tree):
    """
    Remove volume units and replace them with inches.
    """
    if 'cell_count' in tree:
        if tree['cell_count'] > 0:
            n = tree['cell_count']
            tree['runoff'] = tree['runoff-vol'] / n
            tree['et'] = tree['et-vol'] / n
            tree['inf'] = tree['inf-vol'] / n
        else:
            tree['runoff'] = 0
            tree['et'] = 0
            tree['inf'] = 0
        tree.pop('runoff-vol', None)
        tree.pop('et-vol', None)
        tree.pop('inf-vol', None)

    if 'distribution' in tree:
        for subtree in tree['distribution'].values():
            postpass(subtree)


def simulate_modifications(census, fn, cell_res):
    """
    Simulate an entire year, including effects of modifications.

    `census` contains a distribution of cell-types in the area of interest.

    `fn` is as described in `simulate_water_quality`.

    `cell_res` is as described in `simulate_water_quality`.
    """
    mod = create_modified_census(census)
    simulate_water_quality(mod, cell_res, fn)
    postpass(mod)

    unmod = create_unmodified_census(census)
    simulate_water_quality(unmod, cell_res, fn)
    postpass(unmod)

    return {
        'unmodified': unmod,
        'modified': mod
    }


def simulate_year(census, cell_res=10, precolumbian=False):
    """
    Simulate an entire year, including effects of modifications.

    `census` contains a distribution of cell-types in the area of interest.

    `cell_res` is as described in `simulate_water_quality`.

    `precolumbian` is as described in `simulate_cell_year`.
    """
    def fn(cell, cell_count):
        return simulate_cell_year(cell, cell_count, precolumbian)

    return simulate_modifications(census, fn, cell_res)


def simulate_day(census, precip, cell_res=10):
    """
    Simulate a day, including effects of modifications.

    `census` contains a distribution of cell-types in the area of interest.

    `cell_res` is as described in `simulate_water_quality`.

    `precolumbian` is as described in `simulate_cell_year`.
    """
    et_max = 0.207

    def fn(cell, cell_count):
        split = cell.split(':')
        if (len(split) == 2):
            split.append('')
        cell = '%s:%s:%s' % tuple(split[:3])

        land_use = split[1]
        bmp = split[2]
        et = et_max * lookup_ki(bmp or land_use)

        return simulate_cell_day(precip, et, cell, cell_count)

    return simulate_modifications(census, fn, cell_res)
