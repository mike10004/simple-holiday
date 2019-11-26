#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
import unittest
import json
from roundrobin.classic_assigner import Assigner, Shuffler
import roundrobin.tests

_log = logging.getLogger(__name__)


class NonrandomShuffler(Shuffler):

    def __init__(self):
        super().__init__()
    
    def shuffle(self, seq):
        pass

class ClassicAssignerTest(roundrobin.tests.AssignerTestBase):

    def _create_assigner(self):
        return Assigner(self.shuffler)

    def setUp(self):
        self.maxDiff = None
        self.shuffler = NonrandomShuffler()

