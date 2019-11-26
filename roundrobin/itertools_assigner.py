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

    def assign(self, givers, slots, takers=None) -> Dict[Any, Set[Tuple[Any, Any]]]:
        assert len(givers) == len(set(givers))
        assert len(slots) == len(set(slots))
        assert takers is None or (len(takers) == len(set(takers)))
        slots = list(slots)
        takers = takers or set(givers)
        assignments = defaultdict(set)
        for g in givers:
            recipient_pool = self.get_takers(takers, givers, g)
            recipients = self.shuffler.sample(recipient_pool, len(slots))
            for i in range(len(slots)):
                assignments[g].add((slots[i], recipients[i]))
        return dict(assignments.items())
