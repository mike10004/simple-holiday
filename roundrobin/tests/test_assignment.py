#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import unittest
import os
from roundrobin.assignment import Assigner


_log = logging.getLogger(__name__)
_logging_configured = False

if not _logging_configured:
    level = logging.__dict__[os.getenv('SIMPLE_HOLIDAY_TESTS_LOG_LEVEL', 'INFO')]
    logging.basicConfig(level=level)
    _logging_configured = True



class TestAssigner(unittest.TestCase):

    def test_two_people(self):
        a = Assigner()
        actual = a.assign(('A', 'B'), ('*'))
        self.assertEqual(2, len(actual))
        for giver, assignments in actual.items():
            self.assertEqual(1, len(assignments))
            assignment = assignments[0]
            _log.debug("%s is assigned %s", giver, assignment)
            self.assertEqual('*', assignment.slot)
            self.assertNotEqual(giver, assignment.taker)

    def test_three_people(self):
        a = Assigner()
        givers = ('A', 'B', 'C')
        slots = ('*', '$')
        actual = a.assign(givers, slots)
        self.assertEqual(len(givers), len(actual))
        for giver, assignments in actual.items():
            self.assertEqual(2, len(assignments))
            self.assertEqual(set(slots), set([a.slot for a in assignments]))
            self.assertEqual(set(givers) - set([giver]), set([a.taker for a in assignments]))

