# Type definition
from src.core.utils.utilities import Utilities

Matrix = list[list[float]]


class Graph:
  """
  Graph class.
  """

  # Adjacency matrix that represents the graph
  __matrix: Matrix = None

  # Count of graph vertices
  __vertex_count: int = None

  __is_symmetric: bool = None

  __visualization_layout: dict = None

  def __init__(self, matrix: Matrix, layout: dict = None) -> None:
    self.__matrix = matrix
    self.__vertex_count = len(matrix)
    self.__visualization_layout = layout

  @property
  def matrix(self) -> Matrix:
    """ Get the adjacency matrix of the graph """
    return self.__matrix

  @property
  def get_matrix_copy(self) -> Matrix:
    return [row[:] for row in self.matrix]

  @property
  def vertex_count(self) -> int:
    """ Get graph vertices count """
    return self.__vertex_count or 0

  @vertex_count.setter
  def vertex_count(self, value):
    """ Set vertex count value """
    self.__vertex_count = value

  @property
  def is_symmetric(self) -> bool:
    """ Check if graph matrix is symmetric or not """
    if self.__is_symmetric is None:
      self.__is_symmetric = Utilities.is_matrix_symmetric(self.matrix)

    return self.__is_symmetric

  @property
  def layout(self) -> dict | None:
    """ Get saved layout for graph. Check data/input/layout """
    return self.__visualization_layout

  def __len__(self) -> int:
    return len(self.matrix)

  def __str__(self) -> str:
    result = ''

    for row in self.__matrix:
      for weight in row:
        result += f'{weight}\t'

      result += '\n'

    return result
