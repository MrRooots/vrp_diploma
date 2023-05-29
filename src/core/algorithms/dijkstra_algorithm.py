from src.core.interfaces.algorithm import IAlgorithm
from src.core.interfaces.i_vrp_solver import IVRPSolver
from src.core.structures.graph import Graph


class DijkstraAlgorithm(IVRPSolver, IAlgorithm):
  """
  Modified version of Dijkstra's algorithm
  called the "Dijkstra's Algorithm with Node Filtering"

  Complexity
    - [Lists + double for]  -> O(V^2)
    - [Binary Heap (heapq)] -> O(E + V * log(V))

  Where
    - E - number of edges
    - V - number of vertices
  """

  @staticmethod
  def __solver(graph: Graph,
               source: int,
               destination: int | None,
               targets: list[int] | None):
    distances = [float('inf')] * graph.vertex_count
    predecessor = [-1] * graph.vertex_count
    visited = [False] * graph.vertex_count
    distances[source] = 0

    while not (visited[destination] if destination else all(visited)):
      # Find the unvisited node with the smallest distance
      min_vertex = min(
        (u for u in range(graph.vertex_count) if not visited[u]),
        key=lambda x: distances[x]
      )

      visited[min_vertex] = True

      # Update the distances of the neighbors
      for neighbour, weight in enumerate(graph.matrix[min_vertex]):
        if weight is not None and weight > 0 and not visited[neighbour]:
          cost = distances[min_vertex] + weight

          if cost < distances[neighbour]:
            distances[neighbour] = cost
            predecessor[neighbour] = min_vertex

    return distances, predecessor

  @staticmethod
  def __get_path(destination: int,
                 predecessor: list[int]) -> str:
    path, vertex = [], destination

    while vertex != -1:
      path.append(vertex)
      vertex = predecessor[vertex]

    return ' -> '.join(map(str, reversed(path)))

  @staticmethod
  def run(graph: Graph,
          source: int = 0,
          destination: int = None,
          targets: list[int] = None) -> tuple[list, list]:
    distances, predecessor = DijkstraAlgorithm.__solver(graph,
                                                        source=source,
                                                        destination=destination,
                                                        targets=targets)

    return distances, predecessor

  @staticmethod
  def solve_vrp(graph: Graph,
                source: int,
                destination: int,
                targets: list[int]) -> tuple[str, float]:
    distances, predecessor = DijkstraAlgorithm.__solver(graph,
                                                        source,
                                                        destination,
                                                        targets)

    return (
      DijkstraAlgorithm.__get_path(destination, predecessor),
      distances[destination]
    )
