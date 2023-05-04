from src.core.interfaces.i_vrp_solver import IVRPSolver


class BellmanFordWithNodeFiltering(IVRPSolver):
  """
  Modified version of Bellman-Ford's algorithm
  called the "Bellman-Ford Algorithm with Node Filtering"

  Complexity: O(VE)
  E - number of edges
  V - number of vertices
  """
