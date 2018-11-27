#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import random
import logging
import sys
import json
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
        given = defaultdict(list)  # map of giver -> (slot, taker) tuple
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


def tokenize(specs):
    assert isinstance(specs, tuple) or isinstance(specs, list), "expect list or tuple as argument"
    assert len(specs) > 0
    orig = specs
    if len(specs) == 1:
        specs = [s.strip() for s in specs[0].split()]
    _log.debug("tokenized %s to %s", orig, specs)
    return tuple(specs)


def render_assignments(assignments_by_giver, fmt, ofile=sys.stdout):
    if fmt == 'json':
        pretty = {}
        for giver, assmts in assignments_by_giver.items():
            pretty[giver] = [{'to': a[_TAKER], 'kind': a[_SLOT]} for a in assmts]
            json.dump(pretty, ofile, indent=2)
    elif fmt == 'english':
        for giver, assmts in assignments_by_giver.items():
            for a in assmts:
                print("{} gives a \"{}\" gift to {}".format(giver, a[_SLOT], a[_TAKER]), file=ofile)
    else:
        _log.info("bad format %s", fmt)
        raise ValueError("format not allowed")



def main():
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument("givers", nargs='+', help="list of givers")
    p.add_argument("--takers", help="list of takers; givers are used by default")
    p.add_argument("--slots", nargs='+', default='', help="set gift types")
    p.add_argument("--seed", type=int, help="set random number generator seed")
    p.add_argument("--format", choices=('json', 'english'), default='json', help="output format")
    args = p.parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    givers = tokenize(args.givers)
    takers = tokenize(args.takers or givers)
    slots = tokenize(args.slots)
    _log.debug("givers %s; takers %s; slots %s", givers, takers, args.slots)
    all_assignments = Assigner().assign(givers, args.slots, takers)
    render_assignments(all_assignments, args.format)
    return 0

if __name__ == '__main__':
    exit(main())