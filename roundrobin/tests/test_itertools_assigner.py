#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import itertools
import json
from roundrobin.itertools_assigner import ItertoolsAssigner
from roundrobin.tests import NonrandomShuffler
import roundrobin.tests
import roundrobin
from collections import defaultdict
from roundrobin import Assignment

_log = logging.getLogger(__name__)


class ItertoolsAssignerTest(roundrobin.tests.AssignerCaseBase):

    def _create_assigner(self):
        seed = self.seed
        assert seed is not None
        return ItertoolsAssigner(seed)

    def setUp(self):
        self.maxDiff = None
        self.shuffler = NonrandomShuffler()
        self.seed = 3

    def test_repeatable(self):
        accumulated = set()
        first_accumulated = None
        for trial in range(100):
            result = self._do_three_givers_two_slots()
            if first_accumulated is None:
                first_accumulated = result
            accumulated.add(result)
        self.assertSetEqual({first_accumulated}, accumulated)

    def test_6_givers_3_slots(self):
        slots = [1, 2, 3]
        givers = list("abcdef")
        a = self._create_assigner()
        assignment = a.assign(givers, slots)
        self.check_result(assignment, slots)

    def test_many_seeds(self, num_seeds=None):
        n = 0
        counts = defaultdict(list)
        slots = [1, 2, 3]
        givers = list("abcdef")
        if num_seeds is None:
            num_takers_permutations = len(roundrobin.itertools_assigner.Permuter.get_order_changing_permutations(givers))
            num_slots_permutations = len(roundrobin.itertools_assigner.Permuter.get_order_changing_permutations(slots))
            num_seeds = num_takers_permutations * num_slots_permutations
        for seed in range(num_seeds):
            a = ItertoolsAssigner(seed)
            result = a.assign(givers, slots)
            #print("%3d %s" % (seed, str(sorted(result))))
            counts[result].append(seed)
            n += 1
        dupes = 0
        print(n, "seeds checked")
        for ass, seeds in counts.items():
            self.check_result(ass, slots)
            if len(seeds) > 1:
                print(len(seeds), " seeds produce duplicates;", seeds)
                dupes += 1
        print(dupes, "duplicates")
        self.assertEqual(0, dupes, "expect zero seeds produce duplicates")
