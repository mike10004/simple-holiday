#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import unittest
import json
from roundrobin.itertools_assigner import ItertoolsAssigner
from roundrobin.tests import NonrandomShuffler
import roundrobin.tests
import roundrobin
from collections import defaultdict


_log = logging.getLogger(__name__)


class ItertoolsAssignerTest(roundrobin.tests.AssignerCaseBase):

    def _create_assigner(self):
        return ItertoolsAssigner(self.shuffler)

    def setUp(self):
        self.maxDiff = None
        self.shuffler = NonrandomShuffler()

    def test_three_givers_two_slots(self, expected=None):
        expected = expected or {
            'a': {('*', 'c'), ('$', 'b')},
            'b': {('$', 'a'), ('*', 'c')},
            'c': {('*', 'b'), ('$', 'a')},
        }
        super().test_three_givers_two_slots(expected)

    def check_result(self, result, slots, seed, counts=None):
        pre_frozen = set()
        for giver, gifts in result.items():
            received = defaultdict(list)
            for slot, taker in gifts:
                received[slot].append(taker)
            self.assertEqual(len(slots), len(received.keys()), "expect exactly one gift per slot")
            self.assertSetEqual(set(slots), set(received.keys()), "expect giver to give a gift in every slot")
            given_to = []
            for per_slot in received.values():
                given_to += per_slot
            self.assertNotIn(giver, given_to, "expect giver does not self-gift")
            self.assertEqual(len(given_to), len(set(given_to)), "expect no duplicate recipients")
            pre_frozen.add((giver, frozenset(gifts)))
        frozen = frozenset(pre_frozen)
        if counts is not None:
            counts[frozen].append(seed)

    def test_many_seeds(self, num_seeds=None):
        n = 0
        counts = defaultdict(list)
        slots = {1, 2, 3}
        givers = {'a', 'b', 'c', 'd', 'e', 'f'}
        if num_seeds is None:
            num_seeds = roundrobin.Shuffler().count_permutations(len(givers)) #// 2
        for seed in range(num_seeds):
            shuffler = roundrobin.Shuffler(seed)
            a = ItertoolsAssigner(shuffler)
            result = a.assign(givers, slots)
            self.check_result(result, slots, seed, counts)
            n += 1
        dupes = 0
        print(n, "seeds checked")
        for ass, seeds in counts.items():
            if len(seeds) > 1:
                print(len(seeds), " seeds produce duplicates;", seeds)
                dupes += 1
        print(dupes, "duplicates")
    # def test_get_takers(self):
    #     g = 'b'
    #     slot = '*'
    #     already_given_to = {'a'}
    #     takers_slots = {'a': ['*'], 'b': ['*'], 'c': ['$']}
    #     a = self._create_assigner()
    #     recipient_pool = a.get_takers(takers_slots, g, slot, already_given_to)
    #     self.assertListEqual()