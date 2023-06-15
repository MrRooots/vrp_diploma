""" Route improvements. 2-opt """
from src.core.models.problem import Problem
from src.core.utils.utilities import Utilities


class TwoOptAlgorithm:
  """
  2-opt local search implementation.

  Note
    [1]: 2-opt optimization using length_delta

    imp = dist(route[v1], route[v1+1]) - dist(route[v2], route[v2+1]) +
    dist(route[v1+1], route[v2+1]) + dist(route[v1], route[v2])
    If imp < 0 then perform swap. This should save us a lot of computation

  References
    [1]: https://en.wikipedia.org/wiki/2-opt
  """

  @staticmethod
  def __move(tour: list[int], problem: Problem):
    """ Attempt to improve given `sub_tour` """
    best_imp, node1, node2 = 0, -1, -1

    if len(tour) >= 5:
      for i in range(len(tour) - 3):
        for j in range(i + 2, len(tour) - 1):
          new_tour = tour[0:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]

          if Utilities.time_checker(new_tour, problem):
            imp = (problem.matrix[tour[i]][tour[j]] +
                   problem.matrix[tour[i + 1]][tour[j + 1]] -
                   problem.matrix[tour[i]][tour[i + 1]] -
                   problem.matrix[tour[j]][tour[j + 1]])

            if imp < best_imp:
              node1, node2, best_imp = i, j, imp

    return node1, node2, best_imp

  @staticmethod
  def improve(tours: list[list[int]], problem: Problem):
    """
    Attempt to improve all sub-tours in given `tours`
    using 2-opt local search algorithm
    """
    best_imp = 0
    tour = []
    position1 = []
    position2 = []

    for i in range(len(tours)):
      node1, node2, imp = TwoOptAlgorithm.__move(tours[i], problem)

      if node1 != -1:
        best_imp += imp
        tour.append(i)
        position1.append(node1)
        position2.append(node2)

    return tour, position1, position2, best_imp
