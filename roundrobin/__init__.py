

import random
from typing import Sequence, Dict, Tuple, Any, List


class Shuffler(object):

    def __init__(self, seed: int=None):
        if seed is not None:
            self.rng = random.Random(seed)

    def shuffle(self, seq: Sequence):
        self.rng.shuffle(seq)

    def sample(self, seq: Sequence, k: int) -> List:
        """Return a random sample of k elements from a sequence."""
        list_copy = list(seq)
        assert k <= len(list_copy), f"sequence must contain at least k={k} elements"
        self.shuffle(list_copy)
        first_k = list_copy[:k]
        assert len(first_k) == k
        return first_k


class Assigner(object):

    def __init__(self, shuffler: Shuffler):
        self.shuffler = shuffler

    def assign(self, givers, slots, takers=None) -> Dict[Any, List[Tuple[Any, Any]]]:
        raise NotImplementedError("subclasses must implement")