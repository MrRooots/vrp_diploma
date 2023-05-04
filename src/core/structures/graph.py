# Type definition
Matrix = list[list[float]]


class Graph:
  """
  Graph class.
  """

  # Adjacency matrix that represents the graph
  __matrix: Matrix = None

  # Count of graph vertices
  __vertex_count: int = None

  def __init__(self, matrix: Matrix) -> None:
    self.__matrix = matrix
    self.__vertex_count = len(matrix)

  @property
  def matrix(self) -> Matrix:
    """ Get the adjacency matrix of the graph """
    return self.__matrix

  @property
  def vertex_count(self) -> int:
    """ Get graph vertices count """
    return self.__vertex_count or 0

  def __len__(self) -> int:
    return len(self.matrix)

  def __str__(self) -> str:
    result = ''

    for row in self.__matrix:
      for weight in row:
        result += f'{weight}\t'

      result += '\n'

    return result
