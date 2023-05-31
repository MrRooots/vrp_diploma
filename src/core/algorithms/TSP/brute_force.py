from itertools import permutations
from src.core.interfaces.algorithm import IAlgorithm
from src.core.structures.graph import Graph
from src.core.utils.utilities import Utilities


class BruteForceAlgorithm(IAlgorithm):
  """
  Brute-force algorithm implementation

  Examine all possible permutations of cities,
  and keep the one that is shortest

  Complexity
    - O(V!) -> The worst case
  Where
    - V - vertex count
  """

  @staticmethod
  @Utilities.timeit
  def run(graph: Graph, **kwargs) -> tuple[list[int], float]:
    points = range(1, graph.vertex_count)
    best_distance = float('inf')
    best_permutation = None

    for partial_permutation in permutations(points):
      permutation = [0] + list(partial_permutation)
      distance = Utilities.compute_permutation_distance(graph.safe_matrix,
                                                        permutation)

      if distance < best_distance:
        best_distance = distance
        best_permutation = permutation

    return best_permutation, best_distance
