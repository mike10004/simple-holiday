#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import unittest
from roundrobin import Shuffler, Assigner, Assignment
from collections import defaultdict


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


class NonrandomShuffler(Shuffler):

    def __init__(self):
        super().__init__(0)

    def shuffle(self, seq):
        pass


class AssignerCaseBase(unittest.TestCase):

    def _create_assigner(self) -> Assigner:
        raise NotImplementedError("subclasses must implement this method")

    def test_one_person(self):
        a = self._create_assigner()
        a.allow_self_assignment = True
        givers = ('a',)
        actual = a.assign(givers, ('*',))
        expected = {('a', '*', 'a')}
        self.assertSetEqual(expected, actual, "base case (one person, one slot)")

    def test_two_people(self):
        a = self._create_assigner()
        actual = a.assign(('A', 'B'), ('*',))
        expected = {
            ('A', '*', 'B'),
            ('B', '*', 'A'),
        }
        self.assertSetEqual(expected, actual, "two people, one slot")

    def _do_three_givers_two_slots(self):
        a = self._create_assigner()
        givers = ('a', 'b', 'c')
        slots = ('*', '$')
        return a.assign(givers, slots)

    def test_three_givers_two_slots(self, expected: set=None):
        actual = self._do_three_givers_two_slots()
        expected = expected or {
            ('a', '*', 'c'),
            ('a', '$', 'b'),
            ('b', '*', 'a'),
            ('b', '$', 'c'),
            ('c', '*', 'b'),
            ('c', '$', 'a'),
        }
        if expected != actual:
            print("expected: \n\n{}\n\n".format(json.dumps(sorted(expected), cls=BetterEncoder)))
            print("  actual: \n\n{}\n\n".format(json.dumps(sorted(actual.to_set()), cls=BetterEncoder)))
        self.assertSetEqual(expected, actual, "three givers, two slots")

    def check_result(self, result: Assignment, slots):
        slots_by_giver = defaultdict(list)
        slots_by_taker = defaultdict(list)
        takers_by_giver = defaultdict(list)
        for giver, slot, taker in result:
            slots_by_giver[giver].append(slot)
            slots_by_taker[taker].append(slot)
            takers_by_giver[giver].append(taker)
        for giver, slot_list in slots_by_giver.items():
            self.assertListEqual(sorted(slots), sorted(slot_list), "expect giver to give exactly one gift per slot")
        for taker, slot_list in slots_by_taker.items():
            self.assertListEqual(sorted(slots), sorted(slot_list), "expect taker to receive exactly one gift per slot")
        for giver, taker_list in takers_by_giver.items():
            self.assertNotIn(giver, taker_list, "expect giver does not self-gift")
            self.assertEqual(len(taker_list), len(set(taker_list)), "expect no duplicates in taker list: " + str(taker_list))

