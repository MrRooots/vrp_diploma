from itertools import permutations
from src.core.interfaces.algorithm import IAlgorithm
from src.core.structures.graph import Graph


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
  def distance(matrix: list[list[float]],
               permutation: list[int]):
    """ Get path distance for given `permutation` """
    ind1 = permutation
    ind2 = permutation[1:] + permutation[:1]
    distance_sum = 0.0

    for i in range(len(permutation)):
      distance_sum += matrix[ind1[i]][ind2[i]]

    return distance_sum

  @staticmethod
  def run(graph: Graph, **kwargs) -> tuple[list[int], float]:
    points = range(1, graph.vertex_count)
    best_distance = float('inf')
    best_permutation = None

    for partial_permutation in permutations(points):
      permutation = [0] + list(partial_permutation)
      distance = BruteForceAlgorithm.distance(graph.safe_matrix, permutation)

      if distance < best_distance:
        best_distance = distance
        best_permutation = permutation

    return best_permutation, best_distance
