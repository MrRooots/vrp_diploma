from itertools import permutations

from src.core.interfaces.i_tsp_algorithm import ITSPAlgorithm
from src.core.models.result import ResultModel
from src.core.models.tsp_problem import TSPProblem

from src.core.utils.decorators import Decorators
from src.core.utils.utilities import Utilities


class BruteForceAlgorithm(ITSPAlgorithm):
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
  @Decorators.convert_to_result_model
  def run(problem: TSPProblem, **kwargs):
    points = range(1, problem.graph.vertex_count)
    best_distance = float('inf')
    best_permutation = None

    for partial_permutation in permutations(points):
      permutation = [0] + list(partial_permutation)
      distance = Utilities.permutation_distance(problem.graph.safe_matrix,
                                                permutation)

      if distance < best_distance:
        best_distance = distance
        best_permutation = permutation

    return [best_permutation], [best_distance]
