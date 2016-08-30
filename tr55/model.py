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
import numpy as np

from tr55.tablelookup import lookup_cn, lookup_bmp_storage, \
    lookup_ki, is_bmp, is_built_type, make_precolumbian, \
    get_pollutants, get_bmps, lookup_pitt_runoff, lookup_bmp_drainage_ratio
from tr55.water_quality import get_volume_of_runoff, get_pollutant_load
from tr55.operations import dict_plus


def runoff_pitt(precip, evaptrans, soil_type, land_use):
    """
    The Pitt Small Storm Hydrology method.  The output is a runoff
    value in inches.
    This uses numpy to make a linear interpolation between tabular values to
    calculate the exact runoff for a given value

    `precip` is the amount of precipitation in inches.
    """

    runoff_ratios = lookup_pitt_runoff(soil_type, land_use)

    runoff_ratio = np.interp(precip, runoff_ratios['precip'], runoff_ratios['Rv'])
    runoff = precip*runoff_ratio

    return min(runoff, precip - evaptrans)


def nrcs_cutoff(precip, curve_number):
    """
    A function to find the cutoff between precipitation/curve number
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

    `precip` is the amount of precipitation in inches.
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


def simulate_cell_day(precip, evaptrans, cell, cell_count):
    """
    Simulate a bunch of cells of the same type during a one-day event.

    `precip` is the amount of precipitation in inches.

    `evaptrans` is evapotranspiration in inches per day - this is the
    ET for the cell after taking the crop/landscape factor into account
    this is NOT the ETmax.

    `cell` is a string which contains a soil type and land use
    separated by a colon.

    `cell_count` is the number of cells to simulate.

    The return value is a dictionary of runoff, evapotranspiration, and
    infiltration as a volume (inches * #cells).
    """
    def clamp(runoff, et, inf, precip):
        """
        This function ensures that runoff + et + inf <= precip.

        NOTE: Infiltration is normally independent of the
        precipitation level, but this function introduces a slight
        dependency (that is, at very low levels of precipitation, this
        function can cause infiltration to be smaller than it
        ordinarily would be.
        """
        total = runoff + et + inf
        if (total > precip):
            scale = precip / total
            runoff *= scale
            et *= scale
            inf *= scale
        return (runoff, et, inf)

    precip = max(0.0, precip)
    soil_type, land_use, bmp = cell.lower().split(':')

    # If  there  is no  precipitation,  then  there  is no  runoff  or
    # infiltration;  however,  there  is evapotranspiration.   (It  is
    # understood that over a period of  time, this can lead to the sum
    # of the three values exceeding the total precipitation.)
    if precip == 0.0:
        return {
            'runoff-vol': 0.0,
            'et-vol': 0.0,
            'inf-vol': 0.0,
        }

    # If  the BMP  is cluster_housing  or  no_till, then  make it  the
    # land-use.  This is  done because those two types  of BMPs behave
    # more like land-uses than they do BMPs.
    if bmp and not is_bmp(bmp):
        land_use = bmp or land_use

    # When the land-use is a built-type use the Pitt Small Storm Hydrology
    # Model until the runoff predicted by the NRCS model is greater than that
    # predicted by the NRCS model.
    if is_built_type(land_use):
        pitt_runoff = runoff_pitt(precip, evaptrans, soil_type, land_use)
        nrcs_runoff = runoff_nrcs(precip, evaptrans, soil_type, land_use)
        runoff = max(pitt_runoff, nrcs_runoff)
    else:
        runoff = runoff_nrcs(precip, evaptrans, soil_type, land_use)
    inf = max(0.0, precip - (evaptrans + runoff))

    # (runoff, evaptrans, inf) = clamp(runoff, evaptrans, inf, precip)
    return {
        'runoff-vol': cell_count * runoff,
        'et-vol': cell_count * evaptrans,
        'inf-vol': cell_count * inf,
    }


def create_unmodified_census(census):
    """
    This creates a cell census, ignoring any modifications.  The
    output is suitable for use as input to `simulate_water_quality`.
    """
    unmod = copy.deepcopy(census)
    unmod.pop('modifications', None)
    return unmod


def create_modified_census(census):
    """
    This creates a cell census, with modifications, that is suitable
    for use as input to `simulate_water_quality`.

    For every type of cell that undergoes modification, the
    modifications are indicated with a sub-distribution under that
    cell type.
    """
    mod = copy.deepcopy(census)
    mod.pop('modifications', None)

    for (cell, subcensus) in mod['distribution'].items():
        n = subcensus['cell_count']

        changes = {
            'distribution': {
                cell: {
                    'distribution': {
                        cell: {'cell_count': n}
                    }
                }
            }
        }

        mod = dict_plus(mod, changes)

    for modification in (census.get('modifications') or []):
        for (orig_cell, subcensus) in modification['distribution'].items():
            n = subcensus['cell_count']
            soil1, land1 = orig_cell.split(':')
            soil2, land2, bmp = modification['change'].split(':')
            changed_cell = '%s:%s:%s' % (soil2 or soil1, land2 or land1, bmp)

            changes = {
                'distribution': {
                    orig_cell: {
                        'distribution': {
                            orig_cell: {'cell_count': -n},
                            changed_cell: {'cell_count': n}
                        }
                    }
                }
            }

            mod = dict_plus(mod, changes)

    return mod


def simulate_water_quality(tree, cell_res, fn,
                           pct=1.0, current_cell=None, precolumbian=False):
    """
    Perform a water quality simulation by doing simulations on each of
    the cell types (leaves), then adding them together by summing the
    values of a node's subtrees and storing them at that node.

    `tree` is the (sub)tree of cell distributions that is currently
    under consideration.

    `pct` is the percentage of calculated water volume to retain.

    `cell_res` is the size of each cell/pixel in meters squared
     (used for turning inches of water into volumes of water).

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
                simulate_water_quality(subtree, cell_res, fn,
                                       pct, cell, precolumbian)
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
        # the number of cells covered by this leaf
        n = tree['cell_count']

        # canonicalize the current_cell string
        split = current_cell.split(':')
        if (len(split) == 2):
            split.append('')
        if precolumbian:
            split[1] = make_precolumbian(split[1])
        current_cell = '%s:%s:%s' % tuple(split)

        # run the runoff model on this leaf
        result = fn(current_cell, n)  # runoff, et, inf
        runoff_adjustment = result['runoff-vol'] - (result['runoff-vol'] * pct)
        result['runoff-vol'] -= runoff_adjustment
        result['inf-vol'] += runoff_adjustment
        tree.update(result)

        # perform water quality calculation
        if n != 0:
            soil_type, land_use, bmp = split
            runoff_per_cell = result['runoff-vol'] / n
            liters = get_volume_of_runoff(runoff_per_cell, n, cell_res)
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


def compute_bmp_effect(census, m2_per_pixel, precip):
    """
    Compute the overall amount of water retained by infiltration/retention
    type BMP's.

    Result is a percent of runoff remaining after water is trapped in
    infiltration/retention BMP's
    """
    meters_per_inch = 0.0254
    cubic_meters = census['runoff-vol'] * meters_per_inch * m2_per_pixel
    # 'runoff-vol' in census is in inches*#cells
    bmp_dict = census.get('BMPs', {})
    bmp_keys = set(bmp_dict.keys())


    reduction = 0.0
    for bmp in set.intersection(set(get_bmps()), bmp_keys):
        bmp_area = bmp_dict[bmp]
        storage_space = (lookup_bmp_storage(bmp) * bmp_area)
        max_reduction = lookup_bmp_drainage_ratio(bmp) * bmp_area * precip * meters_per_inch
        bmp_reduction = min(max_reduction, storage_space)
        reduction += bmp_reduction

    return 0 if not cubic_meters else \
        max(0.0, cubic_meters - reduction) / cubic_meters


def simulate_modifications(census, fn, cell_res, precip, pc=False):
    """
    Simulate effects of modifications.

    `census` contains a distribution of cell-types in the area of interest.

    `fn` is as described in `simulate_water_quality`.

    `cell_res` is as described in `simulate_water_quality`.
    """
    mod = create_modified_census(census)
    simulate_water_quality(mod, cell_res, fn, precolumbian=pc)
    pct = compute_bmp_effect(mod, cell_res, precip)
    simulate_water_quality(mod, cell_res, fn, pct=pct, precolumbian=pc)
    postpass(mod)

    unmod = create_unmodified_census(census)
    simulate_water_quality(unmod, cell_res, fn, precolumbian=pc)
    postpass(unmod)

    return {
        'unmodified': unmod,
        'modified': mod
    }


def simulate_day(census, precip, cell_res=10, precolumbian=False):
    """
    Simulate a day, including water quality effects of modifications.

    `census` contains a distribution of cell-types in the area of interest.

    `cell_res` is as described in `simulate_water_quality`.

    `precolumbian` indicates that artificial types should be turned
    into forest.
    """
    et_max = 0.207
        # From the EPA WaterSense data finder for the Philadelphia airport (19153)
        # Converted to daily number in inches per day.
        # http://www3.epa.gov/watersense/new_homes/wb_data_finder.html
        # TODO: include Potential Max ET as a data layer from CGIAR
        # http://csi.cgiar.org/aridity/Global_Aridity_PET_Methodolgy.asp

    if 'modifications' in census:
        verify_census(census)

    def fn(cell, cell_count):
        # Compute et for cell type
        split = cell.split(':')
        if (len(split) == 2):
            (land_use, bmp) = split
        else:
            (_, land_use, bmp) = split
        et = et_max * lookup_ki(bmp or land_use)

        # Simulate the cell for one day
        return simulate_cell_day(precip, et, cell, cell_count)

    return simulate_modifications(census, fn, cell_res, precip, precolumbian)


def verify_census(census):
    """
    Assures that there is no soil type/land cover pair
    in a modification census that isn't in the AoI census.
    """
    for modification in census['modifications']:
        for land_cover in modification['distribution']:
            if land_cover not in census['distribution']:
                raise ValueError("Invalid modification census")
