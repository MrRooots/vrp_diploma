from __future__ import annotations

from src.core.interfaces.my_json_serializable import MyJsonSerializable

# Type definition
Matrix = list[list[float]]


class Graph(MyJsonSerializable):
  """
  Graph class.
  """

  # Adjacency matrix that represents the graph
  __matrix: Matrix = None

  # Adjacency matrix with zeros instead of None
  __safe_matrix: Matrix = None

  # Count of graph vertices
  __vertex_count: int = None

  # Symmetric indicator
  __is_symmetric: bool = None

  # Layout for graph points
  __visualization_layout: dict = None

  def __init__(self, matrix: Matrix, layout: dict = None) -> None:
    self.__matrix = matrix
    self.__vertex_count = len(matrix)
    self.__visualization_layout = layout

  def __len__(self) -> int:
    return len(self.matrix)

  def __str__(self) -> str:
    result = ''

    for row in self.__matrix:
      for weight in row:
        result += f'{weight}\t'

      result += '\n'

    return result

  @property
  def matrix(self) -> Matrix:
    """ Get the adjacency matrix of the graph """
    return self.__matrix

  @property
  def safe_matrix(self) -> Matrix:
    """ Get the adjacency matrix with zeros instead of None """
    if self.__safe_matrix is None:
      self.__safe_matrix = [
        [i if i is not None else 0 for i in row]
        for row in self.__matrix
      ]

    return self.__safe_matrix

  @property
  def get_matrix_copy(self) -> Matrix:
    return [row[:] for row in self.matrix]

  @property
  def vertex_count(self) -> int:
    """ Get graph vertices count """
    return self.__vertex_count or 0

  @vertex_count.setter
  def vertex_count(self, value: int) -> None:
    """ Set vertex count value """
    self.__vertex_count = value

  @property
  def layout(self) -> dict | None:
    """ Get saved layout for graph. Check data/input/layout """
    return self.__visualization_layout

  @layout.setter
  def layout(self, value: dict) -> None:
    """ Get saved layout for graph. Check data/input/layout """
    self.__visualization_layout = value

  @property
  def is_symmetric(self) -> bool:
    """ Check if graph matrix is symmetric or not """
    if self.__is_symmetric is None:
      self.__is_symmetric = all(
        self.matrix[i][j] == self.matrix[j][i]
        for i in range(self.vertex_count) for j in range(self.vertex_count)
      )

    return self.__is_symmetric

  def to_json(self) -> dict:
    return {
      'distance_matrix': self.matrix
    }
