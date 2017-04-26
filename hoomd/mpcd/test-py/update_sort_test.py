# Copyright (c) 2009-2017 The Regents of the University of Michigan
# This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

# Maintainer: mphoward

import unittest
import numpy as np
import hoomd
from hoomd import md
from hoomd import mpcd

# unit tests for mpcd.update.sort
class mpcd_update_sort_test(unittest.TestCase):
    def setUp(self):
        # establish the simulation context
        hoomd.context.initialize()

        # default testing configuration
        hoomd.init.read_snapshot(hoomd.data.make_snapshot(N=1, box=hoomd.data.boxdim(L=20.)))

        # initialize the system from the starting snapshot
        self.s = mpcd.init.read_snapshot(mpcd.data.make_snapshot(N=1))

    # test default initialization
    def test_init(self):
        self.assertTrue(self.s is not None)
        # check default period
        self.assertEqual(self.s.sorter.period, 50)
        # check sorter was injected into updater list
        self.assertTrue(self.s.sorter in hoomd.context.current.updaters)

    # test setting period of sorter
    def test_set_period(self):
        self.s.sorter.set_period(period=10)
        self.assertEqual(self.s.sorter.period, 10)

        self.s.sorter.set_period(period=25)
        self.assertEqual(self.s.sorter.period, 25)

    # test enabling / disabling sorter
    def test_disable(self):
        # disabling sorter should remove it from list
        self.s.sorter.disable()
        self.assertFalse(self.s.sorter.enabled)
        self.assertFalse(self.s.sorter in hoomd.context.current.updaters)

        self.s.sorter.enable()
        self.assertTrue(self.s.sorter.enabled)
        self.assertTrue(self.s.sorter in hoomd.context.current.updaters)

    # test that an error is raised if a second sorter gets made
    def test_reinit(self):
        with self.assertRaises(RuntimeError):
            mpcd.update.sort(self.s)

    def tearDown(self):
        del self.s

if __name__ == '__main__':
    unittest.main(argv = ['test.py', '-v'])
