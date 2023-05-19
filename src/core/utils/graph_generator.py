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
  def from_file(filename: str) -> Graph:
    """ Generate `Graph` from given file """
    with open(f'data/input/{filename}', 'r') as file:
      return Graph(matrix=[[float(v) for v in line.split()] for line in file])
