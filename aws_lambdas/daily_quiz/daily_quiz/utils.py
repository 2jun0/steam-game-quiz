import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def divide_randomly(x: Sequence[T], k: int) -> tuple[list[T], list[T]]:
    idxes = range(len(x))

    a_idxes = random.sample(idxes, k=k)
    b_idxes = list(set(idxes) - set(a_idxes))

    a = [x[a_i] for a_i in a_idxes]
    b = [x[b_i] for b_i in b_idxes]

    return a, b
