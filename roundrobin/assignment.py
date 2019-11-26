#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import sys
import json
import csv
from roundrobin import Shuffler
from roundrobin import classic_assigner
from roundrobin import itertools_assigner

_SLOT = 0
_TAKER = 1

_log = logging.getLogger(__name__)
FORMAT_JSON = 'json'
FORMAT_ENGLISH = 'english'
FORMAT_MD_TABLE_TAKERS = 'markdown_takers'
FORMAT_MD_TABLE_SLOTS = 'markdown_slots'
FORMAT_CSV_TAKERS = 'csv_takers'
FORMAT_TSV_TAKERS = 'tsv_takers'
FORMAT_CSV_SLOTS = 'csv_slots'
FORMAT_TSV_SLOTS = 'tsv_slots'
_FORMATS = (
    FORMAT_ENGLISH, 
    FORMAT_JSON, 
    FORMAT_MD_TABLE_TAKERS,
    FORMAT_MD_TABLE_SLOTS,
    FORMAT_CSV_TAKERS,
    FORMAT_TSV_TAKERS,
    FORMAT_CSV_SLOTS,
    FORMAT_TSV_SLOTS,
)

def tokenize(specs):
    assert isinstance(specs, tuple) or isinstance(specs, list), "expect list or tuple as argument"
    assert len(specs) > 0
    orig = specs
    if len(specs) == 1:
        specs = [s.strip() for s in specs[0].split()]
    _log.debug("tokenized %s to %s", orig, specs)
    return tuple(specs)


class AssignmentOracle(object):

    def __init__(self, assignments):
        self.assignments = assignments
    
    def get_taker(self, giver, slot):
        return self.get_by_item(giver, slot, _SLOT)
    
    def get_slot(self, giver, taker):
        return self.get_by_item(giver, taker, _TAKER)

    def get_by_item(self, giver, other, idx, absence_fn=None):
        absence_fn = absence_fn or (lambda x: None)
        assmts = self.assignments.get(giver, [])
        for a in assmts:
            if a[idx] == other:
                for i in range(len(a)):
                    if i != idx:
                        return a[i]
        absence_fn((other, assmts, idx, giver))
        return None
    
    def get_others(self, idx):
        others = set()
        for _, gasses in self.assignments.items():
            for a in gasses:
                others.add(a[idx])
        others = list(others)
        try:
            others = sorted(others)
        except TypeError:
            pass
        return others


class Tabulator(object):

    def __init__(self, other_idx):
        self.other_idx = other_idx
    
    def to_rows(self, givers, assignments):
        oracle = AssignmentOracle(assignments)
        others = oracle.get_others(self.other_idx)
        if set(others) == set(givers):
            others = list(givers)
        cells_per_row = 1 + len(others)
        rows = []
        header_row = tuple([""] + others)
        rows.append(header_row)
        for giver in givers:
            asmts = [oracle.get_by_item(giver, other, self.other_idx) or '' for other in others]
            row_data = tuple([giver] + asmts)
            rows.append(row_data)
        return rows


def _repeat(ch, n):
    return ''.join([ch for i in range(n)])


class MarkdownTableRenderer(object):

    def __init__(self, spaceage):
        self.spaceage = spaceage

    def render(self, rows, ofile=sys.stdout):
        cell_fmt = " %" + str(self.spaceage) + "s "
        width = self.spaceage + 2
        pipe = "|"
        num_cells = len(rows[0])
        divider = pipe + pipe.join([_repeat('-', width) for i in range(num_cells)]) + pipe
        print(divider, file=ofile)
        for row in rows:
            row_formatted = pipe + pipe.join([cell_fmt % row[i] for i in range(len(row))]) + pipe
            print(row_formatted, file=ofile)
            print(divider, file=ofile)


class CsvTableRenderer(object):

    def __init__(self, delimiter):
        self.delimiter = delimiter

    def render(self, rows, ofile=sys.stdout):
        csv_writer = csv.writer(ofile, delimiter=self.delimiter)
        for row in rows:
            csv_writer.writerow(row)


_RENDERABLES = {
    FORMAT_MD_TABLE_TAKERS: (_TAKER, MarkdownTableRenderer, 8),
    FORMAT_MD_TABLE_SLOTS: (_SLOT, MarkdownTableRenderer, 8),
    FORMAT_CSV_TAKERS: (_TAKER, CsvTableRenderer, ","),
    FORMAT_TSV_SLOTS: (_SLOT, CsvTableRenderer, "\t"),
    FORMAT_TSV_TAKERS: (_TAKER, CsvTableRenderer, "\t"),
    FORMAT_CSV_SLOTS: (_SLOT, CsvTableRenderer,  ","),
}

def render_assignments(givers, assignments_by_giver, fmt, ofile=sys.stdout):
    if fmt == FORMAT_JSON:
        pretty = {}
        for giver, assmts in assignments_by_giver.items():
            pretty[giver] = [{'to': a[_TAKER], 'kind': a[_SLOT]} for a in assmts]
            json.dump(pretty, ofile, indent=2)
    elif fmt == FORMAT_ENGLISH:
        for giver in givers:
            for a in assignments_by_giver[giver]:
                print("{} gives a \"{}\" gift to {}".format(giver, a[_SLOT], a[_TAKER]), file=ofile)
    else:
        try:
            rendering_hints = _RENDERABLES[fmt]
        except KeyError:
            _log.info("bad output format %s", fmt)
            raise ValueError("output format invalid")
        other_idx = rendering_hints[0]
        rows = Tabulator(other_idx).to_rows(givers, assignments_by_giver)
        renderer_cls = rendering_hints[1]
        renderer_args = rendering_hints[2:]
        renderer = renderer_cls(*renderer_args)
        renderer.render(rows, ofile)


def main():
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument("givers", nargs='+', help="list of givers")
    p.add_argument("--takers", help="list of takers; givers are used by default")
    p.add_argument("--slots", nargs='+', default='', help="set gift types")
    p.add_argument("--seed", type=int, help="set random number generator seed")
    p.add_argument("--format", choices=_FORMATS, default=_FORMATS[0], help="output format")
    p.add_argument("--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    p.add_argument("--algorithm", choices=('classic', 'nuevo'), default='classic')
    args = p.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    givers = tokenize(args.givers)
    takers = tokenize(args.takers or givers)
    slots = tokenize(args.slots)
    _log.debug("givers %s; takers %s; slots %s", givers, takers, slots)
    shuffler = Shuffler(args.seed)
    if args.algorithm == 'nuevo':
        assigner = itertools_assigner.ItertoolsAssigner(shuffler)
    elif args.algorithm == 'classic':
        assigner = classic_assigner.ClassicAssigner(shuffler)
    else:
        raise ValueError("algorithm not recognized: " + args.algorithm)
    all_assignments = assigner.assign(givers, slots, takers)
    render_assignments(givers, all_assignments, args.format)
    return 0


if __name__ == '__main__':
    exit(main())
