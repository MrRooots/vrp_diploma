from src.core.algorithms.bellman_ford_algorithm import BellmanFordAlgorithm
from src.core.algorithms.dijkstra_algorithm import DijkstraAlgorithm
from src.core.interfaces.algorithm import IAlgorithm
from src.core.interfaces.i_vrp_solver import IVRPSolver
from src.core.structures.graph import Graph


class JohnsonAlgorithm(IVRPSolver, IAlgorithm):
  """
  Johnson's algorithm implementation

  Find the shortest paths between all pairs of vertices in
  an edge-weighted directed graph.

  It allows some edge weights to be negative numbers,
  but no negative-weight cycles may exist.

  It works by using the *Bellman–Ford* algorithm to compute a transformation
  of the input graph that removes all negative weights,
  allowing *Dijkstra's* algorithm to be used on the transformed graph.

  References
    - :class:`DijkstraWithNodeFiltering`
    - :class:`BellmanFordAlgorithm`

  Complexity
    - O(V^2 * log(V) + V * E)

  Where
    - E - number of edges
    - V - number of vertices
  """

  @staticmethod
  def add_fiction_node(graph: Graph) -> None:
    graph.vertex_count += 1
    graph.matrix.append([0] * (graph.vertex_count - 1))
    for v in range(graph.vertex_count):
      graph.matrix[v].append(0)

  @staticmethod
  def remove_fiction_node(graph: Graph) -> None:
    graph.vertex_count -= 1
    del graph.matrix[graph.vertex_count]
    for v in range(graph.vertex_count):
      del graph.matrix[v][graph.vertex_count]

  @staticmethod
  def run(graph: Graph, **kwargs) -> tuple[list, list]:
    """ Applies Johnson's to compute all-pairs shortest paths. """
    n = graph.vertex_count
    JohnsonAlgorithm.add_fiction_node(graph)

    h, _ = BellmanFordAlgorithm.run(graph,
                                    source=graph.vertex_count - 1)

    JohnsonAlgorithm.remove_fiction_node(graph)

    for u in range(n):
      for v in range(n):
        if graph.matrix[u][v] is not None:
          graph.matrix[u][v] += h[u] - h[v]

    distances = [[None for _ in range(n)] for _ in range(n)]
    predecessors = [[None for _ in range(n)] for _ in range(n)]

    for u in range(n):
      distances[u], predecessors[u] = DijkstraAlgorithm.run(graph, source=u)

    for u in range(n):
      for v in range(n):
        if graph.matrix[u][v] is not None:
          delta_h = h[u] - h[v]
          distances[u][v] -= delta_h
          graph.matrix[u][v] -= delta_h

    return distances, predecessors
