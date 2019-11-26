#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from typing import Dict, Tuple, Any, Set, List
import random
import itertools
from roundrobin import Assigner, Shuffler

_log = logging.getLogger(__name__)


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
        takers = self.shuffler.permute(takers)
        circular_takers = itertools.cycle(takers)
        for g in givers:
            for slot in slots:
                recipient = circular_takers.__next__()
                if recipient == g and not self.allow_self_assignment:
                    assert len(givers) > 1
                    recipient = circular_takers.__next__()
                assignments[g][slot] = recipient
        assignments_dict = {}
        for g, gifts in assignments.items():
            assignments_dict[g] = set([(slot, gifts[slot]) for slot in gifts])
        return assignments_dict
