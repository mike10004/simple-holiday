

import random
from typing import Sequence, Dict, Tuple, Any, List
import itertools
from collections import  defaultdict

class Assignment(frozenset):

    def __new__(cls, assignment_dict: Dict[Any, Sequence[Tuple[Any, Any]]]):
        triplets = set()
        for g, gifts in assignment_dict.items():
            for slot, taker in gifts:
                triplets.add((g, slot, taker))
        return super(Assignment, cls).__new__(cls, triplets)

    def to_dict_by_giver(self) -> Dict[Any, List[Tuple[Any, Any]]]:
        d = defaultdict(list)
        for giver, slot, taker in self:
            d[giver].append((slot, taker))
        return d

    @classmethod
    def from_set(cls, triplets):
        return super(Assignment, cls).__new__(cls, triplets)

    def to_set(self):
        return set(self)

class Shuffler(object):

    def __init__(self, seed: int=None):
        self.seed = seed
        if seed is not None:
            self.rng = random.Random(seed)
        else:
            self.rng = random.Random()

    def shuffle(self, seq: Sequence):
        self.rng.shuffle(seq)

    def sample(self, seq: Sequence, k: int) -> List:
        """Return a random sample of k elements from a sequence."""
        list_copy = list(seq)
        assert k <= len(list_copy), "sequence has {} elements but must contain at least k={}".format(len(list_copy), k)
        self.shuffle(list_copy)
        first_k = list_copy[:k]
        assert len(first_k) == k
        return first_k


class Assigner(object):

    def __init__(self):
        self.allow_self_assignment = False

    def assign(self, givers, slots, takers=None) -> Assignment:
        raise NotImplementedError("subclasses must implement")

