class Utilities:
  @staticmethod
  def is_matrix_symmetric(matrix: list[list]) -> bool:
    """ Check if given 2d matrix is symmetric or not """
    length = len(matrix)

    for i in range(length):
      for j in range(length):
        if matrix[i][j] != matrix[j][i]:
          return False

    return True
