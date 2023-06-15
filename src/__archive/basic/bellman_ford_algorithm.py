from src.core.interfaces.algorithm import ITSPAlgorithm
from src.core.interfaces.i_tsp_solver import ITSPSolver
from src.core.models.graph import Graph


class BellmanFordAlgorithm(ITSPSolver, ITSPAlgorithm):
  """
  Modified version of Bellman-Ford's algorithm
  called the "Bellman-Ford Algorithm with Node Filtering"

  Complexity
    - O(V*E) for adjacency list
    - O(V^3) for adjacency matrix

  Where
    - E - number of edges
    - V - number of vertices
  """

  @staticmethod
  def __solver(graph: Graph, source: int):
    pass

  @staticmethod
  def run(problem: Graph, source: int = None) -> tuple[list, list]:
    """ Applies Bellman-Ford to compute single-source shortest paths """
    distances = [float('inf') for _ in range(problem.vertex_count)]
    predecessors: list[int] = [-1 for _ in range(problem.vertex_count)]
    distances[source] = 0

    for relaxation in range(problem.vertex_count - 1):
      for u in range(problem.vertex_count):
        for v in range(problem.vertex_count):
          if problem.matrix[u][v] is not None:
            new_dst = distances[u] + problem.matrix[u][v]
            if new_dst < distances[v]:
              distances[v] = new_dst
              predecessors[v] = u

    if any(
            distances[u] + problem.matrix[u][v] < distances[v]
            for u in range(problem.vertex_count)
            for v in range(problem.vertex_count)
            if problem.matrix[u][v] is not None and problem.matrix[u][v] > 0
    ):
      return [], []

    return distances, predecessors

  @staticmethod
  def solve_tsp(graph: Graph,
                source: int,
                destination: int,
                targets: list[int]):
    pass
