""" Route improvements. 2-opt """
from src.core.models.problem import Problem
from src.core.utils.utilities import Utilities


class OrOptAlgorithm:
  """

  """

  @staticmethod
  def __move(tour: list[int], problem: Problem, opt: int):
    best_imp = 0
    node1, node2, node3 = -1, -1, -1

    if len(tour) >= opt + 3:
      for i in range(len(tour) - opt - 1):
        j = i + opt
        for k in range(len(tour) - 1):
          if (k < i) or (j < k):
            if k < i:
              new_tour = tour[0:k + 1] + tour[i + 1:j + 1] + tour[k + 1:i + 1] + tour[j + 1:]
            else:
              new_tour = tour[0:i + 1] + tour[j + 1:k + 1] + tour[i + 1:j + 1] + tour[k + 1:]

            if Utilities.time_checker(new_tour, problem):
              del_cost = (problem.matrix[tour[i]][tour[i + 1]] +
                          problem.matrix[tour[j]][tour[j + 1]] +
                          problem.matrix[tour[k]][tour[k + 1]])
              imp = (problem.matrix[tour[i]][tour[j + 1]] +
                     problem.matrix[tour[k]][tour[i + 1]] +
                     problem.matrix[tour[j]][tour[k + 1]] -
                     del_cost)

              if imp < best_imp:
                node1, node2, node3 = i, j, k
                best_imp = imp

    return node1, node2, node3, best_imp

  @staticmethod
  def improve(tours: list[list[int]], problem: Problem, k: int):
    best_imp = 0
    tour, position_1, position_2, position_3 = [], [], [], []

    for i in range(len(tours)):
      node1, node2, node3, imp = OrOptAlgorithm.__move(tours[i], problem, k)

      if node1 != -1:
        best_imp += imp
        tour.append(i)
        position_1.append(node1)
        position_2.append(node2)
        position_3.append(node3)

    return tour, position_1, position_2, position_3, best_imp
