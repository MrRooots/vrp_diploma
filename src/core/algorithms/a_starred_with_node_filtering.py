from src.core.structures.graph import Graph


class AStarredWithNodeFiltering(IVehicleRoutingProblemSolver):
  """
  A* Algorithm with Node Filtering

  This algorithm is a modification of Dijkstra's Algorithm that uses a
  heuristic function to guide the search towards the targets.

  Complexity: can be as low as O(E log V) if heuristic function is good enough
  E - number of edges
  V - number of vertices
  """

  @staticmethod
  def solve_vrp(graph: Graph) -> tuple[str, float]:
    pass
