import numpy as np

from src.core.interfaces.algorithm import IAlgorithm
from src.core.structures.graph import Graph


class BellmanHeldKarpAlgorithm(IAlgorithm):
  """
  Bellman–Held–Karp algorithm implementation
  This is dynamic programming algorithm proposed in 1962 independently
  by Bellman and by Held and Karp to solve the traveling salesman problem (TSP),
  in which the input is a distance matrix between a set of cities,
  and the goal is to find a minimum-length tour that visits each
  city exactly once before returning to the starting point.

  It finds the exact solution to this problem, and to several
  related problems including the Hamiltonian cycle problem,
  in exponential time.
  """

  @staticmethod
  def dist(matrix, memo, ni: int, N: frozenset) -> float:
    if not N:
      return matrix[ni][0]

    # Store the costs in the form (nj, dist(nj, N))
    costs = [
      (
        nj,
        matrix[ni][nj] + BellmanHeldKarpAlgorithm.dist(matrix,
                                                       memo,
                                                       nj,
                                                       N.difference({nj}))
      )
      for nj in N
    ]
    nmin, min_cost = min(costs, key=lambda x: x[1])
    memo[(ni, N)] = nmin

    return min_cost

  @staticmethod
  def run(graph: Graph, **kwargs) -> tuple[list[int], float]:
    N = frozenset(range(1, graph.vertex_count))
    memo: dict[tuple, int] = {}

    best_distance = BellmanHeldKarpAlgorithm.dist(graph.safe_matrix,
                                                  memo,
                                                  0,
                                                  N)

    # Step 2: get path with the minimum distance
    ni = 0  # start at the origin
    solution = [0]

    while N:
      ni = memo[(ni, N)]
      solution.append(ni)
      N = N.difference({ni})

    return solution, best_distance
