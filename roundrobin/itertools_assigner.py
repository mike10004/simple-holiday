#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from typing import Dict, Tuple, Any, Set, List, Sequence
import random
import itertools
from roundrobin import Assigner, Shuffler

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


class ItertoolsAssigner(Assigner):

    def __init__(self, shuffler: Shuffler):
        super().__init__(shuffler)

    def get_takers(self, takers_slots, g, slot):
        def is_available(t):
            return (self.allow_self_assignment or g != t) and (slot in takers_slots[t])
        available = filter(is_available, takers_slots.keys())
        return sorted(available)

    def assign(self, givers, slots, takers=None) -> Dict[Any, Set[Tuple[Any, Any]]]:
        assert len(givers) == len(set(givers))
        assert len(slots) == len(set(slots))
        assert takers is None or (len(takers) == len(set(takers)))
        givers = sorted(givers)
        slots = sorted(list(slots))
        takers = sorted(takers or set(givers))
        assignments = defaultdict(dict)
        takers, slots = self.shuffler.permute_two(takers, slots)
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
            assignments_dict[g] = set([(slot, gifts[slot]) for slot in gifts])
        return assignments_dict
