from random import sample

Matrix = list[list[float]]


class Utilities:
  """
  Some useful utilities
  """

  @staticmethod
  def is_matrix_symmetric(matrix: list[list]) -> bool:
    """ Check if given 2d matrix is symmetric or not """
    length = len(matrix)

    return all(
      matrix[i][j] == matrix[j][i]
      for i in range(length) for j in range(length)
    )

  @staticmethod
  def path_to_string(path: list[int], sep: str = ' -> ') -> str:
    """ Convert given path to string: '1 -> 2 -> 3' """
    return sep.join(map(str, path))

  @staticmethod
  def compute_permutation_distance(matrix: Matrix,
                                   permutation: list[int]) -> float:
    """Compute the total route distance of a given permutation

    Notes
    -----
    Suppose the permutation [0, 1, 2, 3], with four nodes. The total distance
    of this path will be from 0 to 1, 1 to 2, 2 to 3, and 3 back to 0. This
    can be fetched from a distance matrix using:

        distance_matrix[ind1, ind2], where
        ind1 = [0, 1, 2, 3]  # the FROM nodes
        ind2 = [1, 2, 3, 0]  # the TO nodes

    This can easily be generalized to any permutation by using ind1 as the
    given permutation, and moving the first node to the end to generate ind2.
    """
    distance, n = 0.0, len(permutation)

    for i in range(n):
      ind1 = permutation[i]
      ind2 = permutation[(i + 1) % n]
      distance += matrix[ind1][ind2]

    return distance

  @staticmethod
  def setup_initial_solution(matrix: Matrix,
                             x0: list = None) -> tuple[list[int], float]:
    """
    Return initial solution and its objective value

    x0 - Permutation with initial solution.
    If `x0` was provided, it is the same list

    fx0 - Objective value of x0
    """

    if not x0:
      n = len(matrix)
      x0 = [0] + sample(range(1, n), n - 1)

    fx0 = Utilities.compute_permutation_distance(matrix, x0)

    return x0, fx0
