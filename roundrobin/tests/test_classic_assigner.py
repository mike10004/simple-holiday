#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import unittest
import json
from roundrobin.classic_assigner import Assigner, Shuffler
import roundrobin.tests

_log = logging.getLogger(__name__)


class BetterEncoder(json.JSONEncoder):

    def default(self, obj):   # pylint: disable=E0202
        if isinstance(obj, set):
           return list(obj)
        return json.JSONEncoder.default(self, obj)


class NonrandomShuffler(Shuffler):

    def __init__(self):
        super().__init__()
    
    def shuffle(self, seq):
        pass

class TestAssigner(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.shuffler = NonrandomShuffler()

    def test_one_person(self):
        a = Assigner(self.shuffler)
        actual = a.assign(('a',), ('*',))
        expected = {
            'a': {('*', 'a')}
        }
        self.assertDictEqual(expected, actual, "base case (one person, one slot)")

    def test_two_people(self):
        a = Assigner(self.shuffler)
        actual = a.assign(('A', 'B'), ('*'))
        expected = {
            'A': {('*', 'B')},
            'B': {('*', 'A')},
        }
        self.assertDictEqual(expected, actual, "two people, one slot")

    def test_three_givers_two_slots(self):
        a = Assigner(self.shuffler)
        givers = ('a', 'b', 'c')
        slots = ('*', '$')
        actual = a.assign(givers, slots)
        expected = {
            'a': {('*', 'c'), ('$', 'b')},
            'b': {('*', 'a'), ('$', 'c')},
            'c': {('*', 'b'), ('$', 'a')},
        }
        if expected != actual:
            print("expected: \n\n{}\n\n".format(json.dumps(expected, cls=BetterEncoder)))
            print("  actual: \n\n{}\n\n".format(json.dumps(actual, cls=BetterEncoder)))
        self.assertDictEqual(expected, actual, "three givers, two slots")


