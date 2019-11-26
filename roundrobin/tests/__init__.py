#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import unittest


_logging_configured = False


if not _logging_configured:
    level = logging.__dict__[os.getenv('SIMPLE_HOLIDAY_TESTS_LOG_LEVEL', 'INFO')]
    logging.basicConfig(level=level)
    _logging_configured = True


class BetterEncoder(json.JSONEncoder):

    def default(self, obj):   # pylint: disable=E0202
        if isinstance(obj, set):
           return list(obj)
        return json.JSONEncoder.default(self, obj)


class AssignerTestBase(unittest.TestCase):

    def _create_assigner(self):
        raise NotImplementedError("subclasses must implement this method")

    def test_one_person(self):
        a = self._create_assigner()
        actual = a.assign(('a',), ('*',))
        expected = {
            'a': {('*', 'a')}
        }
        self.assertDictEqual(expected, actual, "base case (one person, one slot)")

    def test_two_people(self):
        a = self._create_assigner()
        actual = a.assign(('A', 'B'), ('*',))
        expected = {
            'A': {('*', 'B')},
            'B': {('*', 'A')},
        }
        self.assertDictEqual(expected, actual, "two people, one slot")

    def test_three_givers_two_slots(self):
        a = self._create_assigner()
        givers = ('a', 'b', 'c')
        slots = ('*', '$')
        actual = a.assign(givers, slots)
        expected = {
            'a': {('*', 'c'), ('$', 'b')},
            'b': {('*', 'a'), ('$', 'c')},
            'c': {('*', 'b'), ('$', 'a')},
        }
        if expected != actual:
            print("expected: \n\n{}\n\n".format(json.dumps(expected, cls=BetterEncoder)))
            print("  actual: \n\n{}\n\n".format(json.dumps(actual, cls=BetterEncoder)))
        self.assertDictEqual(expected, actual, "three givers, two slots")


