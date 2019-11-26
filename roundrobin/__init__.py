

import random
from typing import Sequence, Dict, Tuple, Any, List
import itertools


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

    def count_permutations(self, num_elements):
        n = 0
        for p in itertools.permutations([None] * num_elements):
            n += 1
        return n

    def permute(self, seq):
        num_permutations = self.count_permutations(len(seq))
        index = self.rng.randint(0, num_permutations - 1) if self.seed is None else (self.seed % num_permutations)
        for i, perm in enumerate(itertools.permutations(seq)):
            if i == index:
                return list(perm)
        raise Exception("shouldn't reach here")

class Assigner(object):

    def __init__(self, shuffler: Shuffler):
        self.shuffler = shuffler
        self.allow_self_assignment = False

    def assign(self, givers, slots, takers=None) -> Dict[Any, List[Tuple[Any, Any]]]:
        raise NotImplementedError("subclasses must implement")
