#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import unittest
import io
import json
from roundrobin import Assignment
from roundrobin.assignment import Tabulator, CsvTableRenderer, MarkdownTableRenderer, AssignmentOracle
from roundrobin.assignment import _TAKER, _SLOT, _FORMATS
from roundrobin.assignment import tokenize, render_assignments
import roundrobin.tests

_log = logging.getLogger(__name__)


class BetterEncoder(json.JSONEncoder):

    def default(self, obj):   # pylint: disable=E0202
        if isinstance(obj, set):
           return list(obj)
        return json.JSONEncoder.default(self, obj)


class TestRenderFunction(unittest.TestCase):

    def test_render_assignments(self):
        sample = Assignment.from_set({
            ('a', '*', 'b'), ('a', '$', 'c'),
            ('b', '*', 'c'), ('b', '$', 'a'),
            ('c', '*', 'a'), ('c', '$', 'b'),
        })
        givers = list(set([x[0] for x in sample]))
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
