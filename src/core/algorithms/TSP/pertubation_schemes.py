"""
Perturbation schemes used in local search-based algorithms.

The functions here receives a permutation list with vertexes from 0 to `n`
and return a generator with all neighbors of this permutation.
"""

from random import sample
from typing import Generator

NeighboursGenerator = Generator[list[int], list[int], None]


def two_opt_gen(x: list[int]) -> NeighboursGenerator:
  """ Perturbation scheme for 2-opt algorithm """
  n = len(x)
  range_i = range(2, n)

  for i in sample(range_i, len(range_i)):
    range_j = range(i + 1, n + 1)

    for j in sample(range_j, len(range_j)):
      xn = x.copy()
      xn = xn[: i - 1] + list(reversed(xn[i - 1: j])) + xn[j:]

      yield xn


# Mapping with all neighborhood generators from this module
neighborhood_gen: dict[str, callable] = {
  'two_opt': two_opt_gen,
}
