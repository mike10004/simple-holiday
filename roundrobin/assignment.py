#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import random
from collections import defaultdict

class SlotAssignment(object):

    def __init__(self, slot, taker):
        self.slot = slot
        assert slot is not None
        self.taker = taker
        assert taker is not None
    
    def __str__(self):
        return "{}/{}".format(self.taker, self.slot)


class Assigner(object):

    def __init__(self):
        pass

    def assign(self, givers, slots, takers=None):
        takers = takers or set(givers)
        givers, takers = list(givers), list(takers)
        slots = list(slots)
        given = defaultdict(list)  # map of giver -> SlotAssignment
        for giver in givers:
            selected_takers = select(set(takers) - set([giver]), len(slots))
            for i in range(len(selected_takers)):
                taker = selected_takers[i]
                slot = slots[i % len(slots)]
                assignment = SlotAssignment(slot, taker)
                given[giver].append(assignment)
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