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
        return ItertoolsAssigner()

    def setUp(self):
        self.maxDiff = None

