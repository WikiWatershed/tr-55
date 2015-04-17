# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import unittest
from tr55.water_quality import get_volume_of_runoff, get_pollutant_load
from tr55.tables import POLLUTION_LOADS


class TestWaterQuality(unittest.TestCase):

    def test_volume(self):
        """
        Test the implementation of the runoff equation.
        """
        cell_res = 30  # meters
        cell_count = 100
        runoff = 0.4  # inches
        liters = get_volume_of_runoff(runoff, cell_count, cell_res)

        self.assertEquals(30480, liters,
                          "Did not calculate the correct runoff volume")

    def test_load(self):
        nlcd = 24
        pollutant = 'tn'
        emc = POLLUTION_LOADS[nlcd][pollutant]
        runoff_liters = 1000

        expected = ((runoff_liters * emc) / 1000000) * 2.205
        load = get_pollutant_load('commercial', pollutant, runoff_liters)

        self.assertEquals(expected, load)

    def test_load_bad_nlcd(self):
        self.assertRaises(Exception, get_pollutant_load, 'asdf', 'tn', 1000)

    def test_load_bad_pollutant(self):
        self.assertRaises(Exception, get_pollutant_load, 'commercial',
                          'asdf', 1000)
