#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import random
import logging
from collections import defaultdict

_SLOT = 0
_TAKER = 1


_log = logging.getLogger(__name__)


class Assigner(object):

    def __init__(self):
        pass

    def assign(self, givers, slots, takers=None):
        takers = takers or set(givers)
        givers, takers = list(givers), list(takers)
        slots = list(slots)
        given = defaultdict(list)  # map of giver -> SlotAssignment
        random.shuffle(takers)
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
                given[giver].append((slot, taker))
        return given


def select(items, n):
    items = list(items)
    random.shuffle(items)
    selected = []
    while len(selected) < n:
        selected.append(items[0])
        del items[0]
    return selected

def do_assignments(givers, takers, slots):
    all_assignments = Assigner().assign(givers, slots, takers)
    print("givers: ", givers)
    print("takers: ", takers)
    print("slots: ", slots)
    for giver, assignments in all_assignments.items():
        print("  {}: ".format(giver), end="")
        for ass in assignments:
            print("{} ".format(str(ass)), end="")
        print()


def list_persons(specs):
    assert len(specs) > 0
    if len(specs) == 1:
        n = int(specs)
        names = []
        for i in range(n):
            names.append("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i])
        return names
    return specs


def main():
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument("givers", nargs='+')
    p.add_argument("--takers")
    p.add_argument("--slots", nargs='+', default='')
    args = p.parse_args()
    givers = list_persons(args.givers)
    takers = list_persons(args.takers or givers)
    do_assignments(givers, takers, args.slots)
    return 0

if __name__ == '__main__':
    exit(main())