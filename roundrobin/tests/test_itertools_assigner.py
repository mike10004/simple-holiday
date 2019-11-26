#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import unittest
import json
from roundrobin.itertools_assigner import ItertoolsAssigner
from roundrobin.tests import NonrandomShuffler
import roundrobin.tests

_log = logging.getLogger(__name__)


class ItertoolsAssignerTest(roundrobin.tests.AssignerCaseBase):

    def _create_assigner(self):
        return ItertoolsAssigner(self.shuffler)

    def setUp(self):
        self.maxDiff = None
        self.shuffler = NonrandomShuffler()

    def test_three_givers_two_slots(self, expected=None):
        expected = expected or {
            'a': {('*', 'c'), ('$', 'b')},
            'b': {('$', 'a'), ('*', 'c')},
            'c': {('*', 'b'), ('$', 'a')},
        }
        super().test_three_givers_two_slots(expected)

