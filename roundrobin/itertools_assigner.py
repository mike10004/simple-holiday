#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from typing import Optional
import roundrobin
import itertools
from roundrobin import Assigner, Assignment

_log = logging.getLogger(__name__)


class Circle(object):

    def __init__(self, items: list, start_after=None):
        self.iterator = itertools.cycle(items)
        if start_after is not None:
            assert start_after in items
            for value in self.iterator:
                if value == start_after:
                    break

    def next(self, prohibited=None):
        value = self.iterator.__next__()
        if prohibited is not None and value == prohibited:
            # if items list has length == 1, then this will be the same value, but that's your fault
            value = self.iterator.__next__()
        return value


class Permuter(object):

    @staticmethod
    def get_order_changing_permutations(seq):
        """
        Gets all permutations of a circular sequence wherein the order is changed.
        :param seq: the sequence
        :return: a list of permutations
        """
        seq = list(seq)
        assert seq
        min_val = min(seq)
        permutations = map(lambda p: tuple(p), itertools.permutations(seq))
        return list(filter(lambda p: p[0] == min_val, permutations))


class ItertoolsAssigner(Assigner):

    def __init__(self, seed: Optional[int]):
        super().__init__()
        self.seed = seed

    def permute_takers_and_slots(self, takers, slots):
        takers_permutations = Permuter.get_order_changing_permutations(takers)
        slots_permutations = list(itertools.permutations(slots))
        takers_perm_index, slots_perm_index = roundrobin.to_multi_seed(self.seed, [len(takers_permutations), len(slots_permutations)])
        return takers_permutations[takers_perm_index], slots_permutations[slots_perm_index]

    def assign(self, givers, slots, takers=None) -> Assignment:
        assert len(givers) == len(set(givers))
        assert len(slots) == len(set(slots))
        assert takers is None or (len(takers) == len(set(takers)))
        givers = sorted(givers)
        slots = sorted(list(slots))
        takers = sorted(takers or set(givers))
        assignments = defaultdict(dict)
        takers, slots = self.permute_takers_and_slots(takers, slots)
        for g in givers:
            if self.allow_self_assignment:
                prohibited = None
            else:
                prohibited = g
                assert len(takers) > 1, "must allow self-assignment if list of recipients has length 1"
            takers_circle = Circle(takers, g)
            for slot in slots:
                recipient = takers_circle.next(prohibited)
                assignments[g][slot] = recipient
        assignments_dict = {}
        for g, gifts in assignments.items():
            assignments_dict[g] = [(slot, gifts[slot]) for slot in gifts]
        return Assignment(assignments_dict)
