# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from tr55.tablelookup import lookup_load, lookup_nlcd


def get_volume_of_runoff(runoff, cell_count, cell_resolution):
    """
    Calculate the volume of runoff over the entire modeled area

    Args:
        runoff (number): Q from TR55, averaged amount of runoff over a number
        of cells.

        cell_count (integer): The number of cells included in the area

        cell_resolution (number): The size in square meters that a cell
        represents

    Returns:
        The volume of runoff liters in of the total area of interest
    """

    # Runoff is in inches, so convert to meters which is the units for the cell
    # area and compute the meter-cells in the group.  Multiply the resolution
    # of the cell to get the runoff volume in cubic meters.
    inch_to_meter = 0.0254

    runoff_m = runoff * inch_to_meter
    meter_cells = runoff_m * cell_count
    volume_cubic_meters = meter_cells * cell_resolution

    liters = volume_cubic_meters * 1000

    return liters


def get_pollutant_load(use_type, pollutant, runoff_liters):
    """
    Calculate the pollutant load over a particular land use type given an
    amount of runoff generated on that area and an event mean concentration
    of the pollutant.  Returns the pollutant load in lbs.
    """
    mg_per_kg = 1000000
    lbs_per_kg = 2.205

    nlcd = lookup_nlcd(use_type)
    emc = lookup_load(nlcd, pollutant)

    load_mg_l = emc * runoff_liters

    return (load_mg_l / mg_per_kg) * lbs_per_kg
