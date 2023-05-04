from src.core.structures.graph import Graph


class GraphGenerator:
  """
  GraphGenerator class.
  """

  @staticmethod
  def from_adjacency_matrix(matrix: list[list[float]]) -> Graph:
    """ Generate `Graph` from given `matrix` """
    return Graph(matrix)

  @staticmethod
  def from_adjacency_list(connections: dict[str, tuple[tuple[str, float]]]) -> Graph:
    """ Generate `Graph` from given dict of connections """
    pass

  @staticmethod
  def from_file(filename: str) -> Graph:
    """ Generate `Graph` from given file """
    matrix = []

    with open(f'data/{filename}', 'r') as file:
      while line := file.readline():
        matrix.append([])

        for vertex in line.split():
          matrix[-1].append(float(vertex))

      return Graph(matrix=matrix)
