#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from typing import Dict, Tuple, Any, Sequence
import random

_log = logging.getLogger(__name__)

class Shuffler(object):

    def __init__(self, seed: int=None):
        if seed is not None:
            self.rng = random.Random(seed)

    def shuffle(self, seq: Sequence):
        self.rng.shuffle(seq)


class Assigner(object):

    def __init__(self, shuffler: Shuffler):
        self.shuffler = shuffler

    def assign(self, givers, slots, takers=None) -> Dict[Any, Tuple[Any, Any]]:
        takers = takers or set(givers)
        givers, takers = list(givers), list(takers)
        slots = list(slots)
        try:
            givers = sorted(givers)
            takers = sorted(takers)
            slots = sorted(slots)
        except TypeError:
            pass
        given = defaultdict(set)  # map of giver -> set of (slot, taker) tuples
        self.shuffler.shuffle(takers)
        _log.debug("shuffled takers: %s", takers)
        for giver in givers:
            i0 = takers.index(giver)
            p_takers = []
            indexes = [i % len(takers) for i in range(i0 + 1, i0 + 1 + len(slots))]
            _log.debug("giver %s is index %s among takers %s; examining elements %s of takers", giver, i0, takers, indexes)
            for i in indexes:
                p_takers.append(takers[i])
            _log.debug("p_takers %s for slots %s", p_takers, slots)
            assert len(slots) == len(p_takers), "expect to have one assigned taker per slot, but we have {} takers for {} slots".format(len(p_takers), len(slots))
            for i in range(len(p_takers)):
                slot, taker = slots[i], p_takers[i]
                given[giver].add((slot, taker))
        return dict(given.items())


