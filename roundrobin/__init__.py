

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

    # @classmethod
    # def _equals_with_offset(cls, p, q, q_offset):
    #     for i in range(len(p)):
    #         if p[i] != q[(i + q_offset) % len(q)]:
    #             return False
    #     return True
    #
    # @classmethod
    # def same_order(cls, p, q):
    #     assert len(p) == len(q)
    #     n = len(p)
    #     for q_offset in range(n):
    #         if not Shuffler._equals_with_offset(p, q, q_offset):
    #             return False
    #     return True

    @classmethod
    def get_order_changing_permutations(cls, seq):
        seq = list(seq)
        assert seq
        min_val = min(seq)
        permutations = map(lambda p: tuple(p), itertools.permutations(seq))
        return list(filter(lambda p: p[0] == min_val, permutations))

    def permute_two(self, seq1, seq2):
        all_perms_1 = Shuffler.get_order_changing_permutations(seq1)
        all_perms_2 = Shuffler.get_order_changing_permutations(seq2)
        index_pairs_list = list(itertools.product(list(range(len(all_perms_1))), list(range(len(all_perms_2)))))
        index_pairs_list_len = len(index_pairs_list)
        index = self.rng.randint(0, index_pairs_list_len - 1) if self.seed is None else (self.seed % index_pairs_list_len)
        index1, index2 = index_pairs_list[index]
        seq1_perm = all_perms_1[index1]
        seq2_perm = all_perms_2[index2]
        return seq1_perm, seq2_perm
        #return seq1_perm, seq2   # TODO really use the seq2 perm; this is a stand-in


class Assigner(object):

    def __init__(self, shuffler: Shuffler):
        self.shuffler = shuffler
        self.allow_self_assignment = False

    def assign(self, givers, slots, takers=None) -> Dict[Any, List[Tuple[Any, Any]]]:
        raise NotImplementedError("subclasses must implement")
