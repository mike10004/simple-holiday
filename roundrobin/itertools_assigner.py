#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from typing import Dict, Tuple, Any, Sequence
import random
import itertools


_log = logging.getLogger(__name__)


class ItertoolsAssigner(object):

    def assign(self, givers, slots, takers=None) -> Dict[Any, Tuple[Any, Any]]:
        assert len(givers) == len(set(givers))
        assert len(slots) == len(set(slots))
        takers = takers or set(givers)
        for g in givers:
            recipient_pool = list(filter(lambda t: t != g, takers))
        raise NotImplementedError()
