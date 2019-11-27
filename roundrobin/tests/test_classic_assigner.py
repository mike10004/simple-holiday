#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging
from roundrobin.classic_assigner import ClassicAssigner
from roundrobin.tests import NonrandomShuffler
import roundrobin.tests


_log = logging.getLogger(__name__)


class ClassicAssignerTest(roundrobin.tests.AssignerCaseBase):

    def _create_assigner(self):
        return ClassicAssigner(self.shuffler)

    def setUp(self):
        self.maxDiff = None
        self.shuffler = NonrandomShuffler()

