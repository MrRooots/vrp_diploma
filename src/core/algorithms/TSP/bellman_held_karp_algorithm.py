from functools import lru_cache

from src.core.interfaces.i_tsp_algorithm import ITSPAlgorithm
from src.core.models.result import ResultModel
from src.core.models.tsp_problem import TSPProblem
from src.core.utils.decorators import Decorators


class BellmanHeldKarpAlgorithm(ITSPAlgorithm):
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
  @Decorators.convert_to_result_model
  def run(problem: TSPProblem, **kwargs):
    vertexes: frozenset[int] = frozenset(range(1, problem.graph.vertex_count))
    memory: dict[tuple, int] = {}

    @lru_cache(maxsize=None)
    def dist(current_vertex: int, vertexes: frozenset) -> float:
      """
      Recursively find all distances from `current_vertex`
      to all vertexes in `vertexes` set and save calculated distances
      into `memory` dict.

      The smallest one will be returned

      Note
        Function is wrapped with @lru_cache decorator,
        that saves function most recent calls.
        When function called with already used arguments the cached result
        will be returned instead of function execution
      """
      if not vertexes:
        return problem.graph.safe_matrix[current_vertex][0]

      # Store the costs in the form (nj, dist(nj, N))
      costs = [(
        nj,
        problem.graph.safe_matrix[current_vertex][nj] + dist(nj, vertexes.difference({nj}))
      ) for nj in vertexes]
      minimum_vertex, min_cost = min(costs, key=lambda x: x[1])
      memory[(current_vertex, vertexes)] = minimum_vertex

      return min_cost

    # Get the best path distance
    best_distance = dist(0, vertexes)

    current_vertex, solution = 0, [0]

    # Restore the shortest path in a form of vertex array
    while vertexes:
      current_vertex = memory[(current_vertex, vertexes)]
      solution.append(current_vertex)
      vertexes = vertexes.difference({current_vertex})

    return [solution], [best_distance]
