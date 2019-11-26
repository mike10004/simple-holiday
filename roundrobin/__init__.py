

import random
from typing import Sequence, Dict, Tuple, Any


class Shuffler(object):

    def __init__(self, seed: int=None):
        if seed is not None:
            self.rng = random.Random(seed)

    def shuffle(self, seq: Sequence):
        self.rng.shuffle(seq)


class Assigner(object):

    def __init__(self, shuffler: Shuffler):
        self.shuffler = shuffler

    def assign(self, givers, slots, takers=None) -> Dict[Any, Tuple[Any, Any]]:
        raise NotImplementedError("subclasses must implement")