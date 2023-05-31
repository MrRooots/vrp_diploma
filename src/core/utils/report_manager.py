from src.core.structures.graph import Graph


class ReportManager:
  """
  Class controls the creation report for different cases
  """

  @staticmethod
  def restore_paths(graph: Graph, predecessors: list[list[int]]):
    """
    Restores the paths from the source vertex to all destinations
    using the parent array obtained from Dijkstra's algorithm.
    """
    paths = {}

    for vertex in range(graph.vertex_count):
      path = []
      current = vertex

      while current is not None:
        path.append(current)
        current = predecessors[current]

      path.reverse()
      paths[vertex] = path

    return paths

  @staticmethod
  def make_report_from_complete_data(path: list[int], cost: float) -> None:
    print(
      f'The shortest path with cost = {cost} is: {"->".join(map(str, path))}'
    )

  @staticmethod
  def make_report(graph: Graph,
                  distances: list[list[float]],
                  predecessors: list[list[int]],
                  source: int = 0,
                  destination: int = None,
                  targets: list[int] = None) -> None:
    """ Create report """
    print('Distances:')
    for v in range(graph.vertex_count):
      try:
        print(f"From {v} to")
        for i, length in enumerate(distances[v]):
          print(f'\t\t  {i} => {length if length != float("inf") else "No path"}')
      except TypeError:
        print(f"From {source} to {v} is: {distances[v]}")

    print('Paths:')
    predecessors = [[i if i != -1 else 0 for i in path] for path in predecessors]
    try:
      for _source in range(graph.vertex_count):
        for _destination in range(graph.vertex_count):
          if _source == _destination:
            continue

          path = [_source]
          while path[-1] != _destination:
            next_vertex = predecessors[path[-1]][_destination]
            if next_vertex is None:
              break
            path.append(next_vertex)

          if len(path) > 1 and path[-1] == _destination:
            p = '->'.join(map(str, path)) if distances[_source][_destination] != float('inf') else 'No path'
            print(f"Shortest path from {_source} to {_destination} ({distances[_source][_destination]}): {p}")
    except TypeError:
      for i, path in enumerate(ReportManager.restore_paths(graph, predecessors).values()):
        print(f'Path from {source} to {i} is: {"->".join(map(str, path))}')
