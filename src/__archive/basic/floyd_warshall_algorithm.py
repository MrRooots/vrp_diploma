from src.core.interfaces.algorithm import ITSPAlgorithm
from src.core.models.graph import Graph

FloatMatrix: list[list[float]]
NullableIntMatrix: list[list[int]]


class FloydWarshallAlgorithm(ITSPAlgorithm):
  """
  Floyd-Warshall algorithm implementation

  Finding shortest paths in a directed weighted graph
  with positive or negative edge weights (but with no negative cycles).

  A single execution of the algorithm will find the lengths (summed weights)
  of shortest paths between all pairs of vertices.

  Complexity
    - O(V^3)

  Where
    - V - number of vertices
  """

  @staticmethod
  def run(problem: Graph, **kwargs) -> tuple[list, list]:
    distances: FloatMatrix = [
      [float('inf')] * problem.vertex_count
      for _ in range(problem.vertex_count)
    ]
    predecessor: NullableIntMatrix = [
      [-1] * problem.vertex_count
      for _ in range(problem.vertex_count)
    ]

    for row in range(problem.vertex_count):
      distances[row][row] = 0
      for v in range(problem.vertex_count):
        if problem.matrix[row][v] is not None:
          distances[row][v] = problem.matrix[row][v]
          predecessor[row][v] = v

    for k in range(problem.vertex_count):
      for row in range(problem.vertex_count):
        for v in range(problem.vertex_count):
          new_distance = distances[row][k] + distances[k][v]

          if new_distance < distances[row][v]:
            distances[row][v] = new_distance
            predecessor[row][v] = predecessor[row][k]

    # Check for negative weight cycles
    if any(distances[u][u] < 0 for u in range(problem.vertex_count)):
      return [], []

    return distances, predecessor
