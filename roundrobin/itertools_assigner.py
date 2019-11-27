#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from typing import Dict, Tuple, Any, Set, List, Optional
import random
import itertools
from roundrobin import Assigner, Assignment, Shuffler

_log = logging.getLogger(__name__)


class Circle(object):

    def __init__(self, items: List):
        self.iterator = itertools.cycle(items)

    def next(self, prohibited=None):
        value = self.iterator.__next__()
        if prohibited is not None and value == prohibited:
            # if items list has length == 1, then this will be the same value, but that's your fault
            value = self.iterator.__next__()
        return value


class Permuter(object):

    @staticmethod
    def get_order_changing_permutations(seq):
        seq = list(seq)
        assert seq
        min_val = min(seq)
        permutations = map(lambda p: tuple(p), itertools.permutations(seq))
        return list(filter(lambda p: p[0] == min_val, permutations))

    # def permute_two(self, seq1, seq2):
    #     all_perms_1 = Permuter.get_order_changing_permutations(seq1)
    #     all_perms_2 = Permuter.get_order_changing_permutations(seq2)
    #     index_pairs_list = list(itertools.product(list(range(len(all_perms_1))), list(range(len(all_perms_2)))))
    #     index_pairs_list_len = len(index_pairs_list)
    #     if self.seed is None:
    #         random.Random().randint(0, index_pairs_list_len - 1)
    #     else:
    #         index = self.seed % index_pairs_list_len
    #     index1, index2 = index_pairs_list[index]
    #     seq1_perm = all_perms_1[index1]
    #     seq2_perm = all_perms_2[index2]
    #     return seq1_perm, seq2_perm



class ItertoolsAssigner(Assigner):

    def __init__(self, seed: Optional[int]):
        super().__init__()
        self.seed = seed

    def permute_takers_and_slots(self, takers, slots):
        takers_permutations = Permuter.get_order_changing_permutations(takers)
        slots_permutations = list(itertools.permutations(slots))
        index_pairs = list(itertools.product(list(range(len(takers_permutations))), list(range(len(slots_permutations)))))
        if self.seed is None:
            takers_perm_index, slots_perm_index = index_pairs[random.randint(0, len(index_pairs) - 1)]
        else:
            takers_perm_index, slots_perm_index = index_pairs[self.seed % len(index_pairs)]
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
        takers_circle = Circle(takers)
        for g in givers:
            if self.allow_self_assignment:
                prohibited = None
            else:
                prohibited = g
                assert len(takers) > 1, "must allow self-assignment if list of recipients has length 1"
            for slot in slots:
                recipient = takers_circle.next(prohibited)
                assignments[g][slot] = recipient
        assignments_dict = {}
        for g, gifts in assignments.items():
            assignments_dict[g] = [(slot, gifts[slot]) for slot in gifts]
        return Assignment(assignments_dict)
