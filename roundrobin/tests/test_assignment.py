#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import unittest
import os
import io
import random
import json
from roundrobin.assignment import Assigner, Tabulator, CsvTableRenderer, MarkdownTableRenderer, AssignmentOracle, Shuffler
from roundrobin.assignment import _TAKER, _SLOT, _FORMATS
from roundrobin.assignment import tokenize, render_assignments

_log = logging.getLogger(__name__)
_logging_configured = False

if not _logging_configured:
    level = logging.__dict__[os.getenv('SIMPLE_HOLIDAY_TESTS_LOG_LEVEL', 'INFO')]
    logging.basicConfig(level=level)
    _logging_configured = True


class BetterEncoder(json.JSONEncoder):

    def default(self, obj):   # pylint: disable=E0202
        if isinstance(obj, set):
           return list(obj)
        return json.JSONEncoder.default(self, obj)


class NonrandomShuffler(Shuffler):

    def __init__(self):
        pass
    
    def shuffle(self, seq):
        pass

class TestAssigner(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.shuffler = NonrandomShuffler()

    def test_one_person(self):
        a = Assigner(self.shuffler)
        actual = a.assign(('a'), ('*'))
        expected = {
            'a': set([('*', 'a')])
        }
        self.assertDictEqual(expected, actual, "base case (one person, one slot)")

    def test_two_people(self):
        a = Assigner(self.shuffler)
        actual = a.assign(('A', 'B'), ('*'))
        expected = {
            'A': set([('*', 'B')]),
            'B': set([('*', 'A')]),
        }
        self.assertDictEqual(expected, actual, "two people, one slot")

    def test_three_givers_two_slots(self):
        a = Assigner(self.shuffler)
        givers = ('a', 'b', 'c')
        slots = ('*', '$')
        actual = a.assign(givers, slots)
        expected = {
            'a': set([('*', 'c'), ('$', 'b')]),
            'b': set([('*', 'a'), ('$', 'c')]),
            'c': set([('*', 'b'), ('$', 'a')]),
        }
        if expected != actual:
            print("expected: \n\n{}\n\n".format(json.dumps(expected, cls=BetterEncoder)))
            print("  actual: \n\n{}\n\n".format(json.dumps(actual, cls=BetterEncoder)))
        self.assertDictEqual(expected, actual, "three givers, two slots")


class TestRenderFunction(unittest.TestCase):

    def test_render_assignments(self):
        sample = {
            'a': [('*', 'b'), ('$', 'c')],
            'b': [('*', 'c'), ('$', 'a')],
            'c': [('*', 'a'), ('$', 'b')],
        }
        givers = list(sample.keys())
        for fmt in _FORMATS:
            ofile = io.StringIO()
            render_assignments(givers, sample, fmt, ofile)
            output = ofile.getvalue()
            _log.debug("rendered %s: \n%s\n", fmt, output)
            self.assertTrue(bool(output.strip()), "expect nonempty output")


class TestTokenizer(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(("A", "B", "C"), tokenize(["A B C"]))
        self.assertEqual(("A", "B", "C"), tokenize(("A", "B", "C")))
        self.assertEqual(("A",), tokenize(["A"]))


class TestAssignmentOracle(unittest.TestCase):

    def test_get_others(self):
        sample = {
            'a': [('*', 'b'), ('$', 'c')],
            'b': [('*', 'c'), ('$', 'a')],
            'c': [('*', 'a'), ('$', 'b')],
        }
        oracle = AssignmentOracle(sample)
        takers = oracle.get_others(_TAKER)
        self.assertListEqual(['a', 'b', 'c'], takers)
        slots = oracle.get_others(_SLOT)
        self.assertListEqual(['$', '*'], slots)



class TestTabulator(unittest.TestCase):

    sample = {
        'a': [('*', 'b'), ('$', 'c')],
        'b': [('*', 'c'), ('$', 'a')],
        'c': [('*', 'a'), ('$', 'b')],
    }

    def test_to_rows_takers(self):
        renderer = Tabulator(_TAKER)
        rows = renderer.to_rows(sorted(list(self.sample.keys())), self.sample)
        expected = [
            ('', 'a', 'b', 'c'),
            ('a', '', '*', '$'),
            ('b', '$', '', '*'),
            ('c', '*', '$', ''),
        ]
        self.assertEqual(expected, rows)

    def test_to_rows_slots(self):
        renderer = Tabulator(_SLOT)
        rows = renderer.to_rows(sorted(list(self.sample.keys())), self.sample)
        expected = [
            ('', '$', '*'),
            ('a', 'c', 'b'),
            ('b', 'a', 'c'),
            ('c', 'b', 'a'),
        ]
        self.assertEqual(expected, rows)


class TestMarkdownTableRenderer(unittest.TestCase):

    def test_render(self):
        rows = [
            ('', 'a', 'b', 'c'),
            ('a', '', '*', '$'),
            ('b', '$', '', '*'),
            ('c', '*', '$', ''),
        ]
        ofile = io.StringIO()
        MarkdownTableRenderer(1).render(rows, ofile)
        output = ofile.getvalue()
        expected = """\
|---|---|---|---|
|   | a | b | c |
|---|---|---|---|
| a |   | * | $ |
|---|---|---|---|
| b | $ |   | * |
|---|---|---|---|
| c | * | $ |   |
|---|---|---|---|
"""
        self.assertEqual(expected, output)

class TestCsvTableRenderer(unittest.TestCase):

    def test_render(self):
        rows = [
            ('', 'a', 'b', 'c'),
            ('a', '', '*', '$'),
            ('b', '$', '', '*'),
            ('c', '*', '$', ''),
        ]
        ofile = io.StringIO()
        CsvTableRenderer(',').render(rows, ofile)
        output = ofile.getvalue()
        expected = [
            ",a,b,c",
            "a,,*,$",
            "b,$,,*",
            "c,*,$,",
            "",
        ]
        EOL = "\r\n"
        expected = EOL.join(expected)
        self.assertEqual(expected, output)
