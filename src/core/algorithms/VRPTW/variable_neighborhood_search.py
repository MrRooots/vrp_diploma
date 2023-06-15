from src.core.optimization.two_opt import TwoOptAlgorithm
from src.core.optimization.two_opt_star import two_optstar_search
from src.core.optimization.or_opt import OrOptAlgorithm
from src.core.optimization.relocation import relocate_search

from src.core.models.problem import Problem


class VariableNeighborhoodSearch:
  """
  Variable neighborhood search implementation.

  Method proposed by Mladenović & Hansen in 1997, is a metaheuristic method
  for solving a set of combinatorial optimization and global optimization problems.

  VNS - heuristic designed to tune by combining a partial search algorithms
  that may provide a sufficiently good solution to an optimization problem.

  It explores distant neighborhoods of the current solution, and moves
  from there to a new one if and only if an improvement was made.
  The local search method is applied repeatedly to get from solutions
  in the neighborhood to local optima.
  """

  @staticmethod
  def __apply_two_opt(sub_tour, tour, position1, position2):
    """ Apply 2-opt to given tour """
    for t in range(len(tour)):
      _tour = sub_tour[tour[t]]
      new_tour = (_tour[0:position1[t] + 1] +
                  _tour[position1[t] + 1:position2[t] + 1][::-1] +
                  _tour[position2[t] + 1:])

      sub_tour[_tour[t]] = new_tour

    return sub_tour, tour, position1, position2

  @staticmethod
  def __apply_or_opt(sub_tour, tour, position1, position2, position3):
    for t in range(len(tour)):
      tour = sub_tour[tour[t]]
      if position3[t] < position1[t]:
        new_tour = (tour[:position3[t] + 1] +
                    tour[position1[t] + 1:position2[t] + 1] +
                    tour[position3[t] + 1:position1[t] + 1] +
                    tour[position2[t] + 1:])
      else:
        new_tour = (tour[:position1[t] + 1] +
                    tour[position2[t] + 1:position3[t] + 1] +
                    tour[position1[t] + 1:position2[t] + 1] +
                    tour[position3[t] + 1:])

      sub_tour[tour[t]] = new_tour

    return sub_tour, tour, position1, position2, position3

  @staticmethod
  def __apply_opt_star(sub_tour, tour1, tour2, position1, position2):
    new_tour1 = sub_tour[tour1][:position1 + 1] + sub_tour[tour2][position2 + 1:]
    new_tour2 = sub_tour[tour2][:position2 + 1] + sub_tour[tour1][position1 + 1:]
    sub_tour[tour1] = new_tour1
    sub_tour[tour2] = new_tour2

    return sub_tour, tour1, tour2, position1, position2

  @staticmethod
  def optimize_tour(sub_tour: list[list[int]],
                    problem: Problem,
                    neighbours: list[int]) -> None:
    """ Execute VNS for given `tour`. """
    nb_no_imp = 0
    improvement = float("inf")
    neighbor_order = neighbours
    neighbor_str = 0
    stop = False
    (tour, tour1, tour2,
     position_1, position_2, position_3,
     insert_position, customer) = [None] * 8

    while not stop:
      # 2-opt
      if neighbor_order[neighbor_str] == 0:
        __tour, position_1, position_2, improvement = TwoOptAlgorithm.improve(sub_tour, problem)

      # Or-opt-1 | Or-opt-2 | Or-opt-3
      elif neighbor_order[neighbor_str] in (1, 2, 3):
        k = neighbor_order[neighbor_str]
        __tour, position_1, position_2, position_3, improvement = OrOptAlgorithm.improve(sub_tour, problem, k)

      # 2-opt*
      elif neighbor_order[neighbor_str] == 4:
        __tour1, __tour2, position_1, position_2, improvement = two_optstar_search(sub_tour, problem)

      # Relocation
      elif neighbor_order[neighbor_str] == 5:
        __tour1, __tour2, customer, insert_position, improvement = relocate_search(sub_tour, problem)

      if round(improvement, 5) < 0:
        # 2-opt
        if neighbor_order[neighbor_str] == 0:
          for t in range(len(__tour)):
            tour = sub_tour[__tour[t]]
            sub_tour[__tour[t]] = (tour[0:position_1[t] + 1] +
                                   tour[position_1[t] + 1:position_2[t] + 1][::-1] +
                                   tour[position_2[t] + 1:])

        # Or-opt
        elif neighbor_order[neighbor_str] in (1, 2, 3):
          for t in range(len(__tour)):
            tour = sub_tour[__tour[t]]

            if position_3[t] < position_1[t]:
              new_tour = (tour[:position_3[t] + 1] +
                          tour[position_1[t] + 1:position_2[t] + 1] +
                          tour[position_3[t] + 1:position_1[t] + 1] +
                          tour[position_2[t] + 1:])
            else:
              new_tour = (tour[:position_1[t] + 1] +
                          tour[position_2[t] + 1:position_3[t] + 1] +
                          tour[position_1[t] + 1:position_2[t] + 1] +
                          tour[position_3[t] + 1:])

            sub_tour[__tour[t]] = new_tour

        # 2-opt*
        elif neighbor_order[neighbor_str] == 4:
          new_tour_1 = sub_tour[__tour1][:position_1 + 1] + sub_tour[__tour2][position_2 + 1:]
          new_tour_2 = sub_tour[__tour2][:position_2 + 1] + sub_tour[__tour1][position_1 + 1:]
          sub_tour[__tour1] = new_tour_1
          sub_tour[__tour2] = new_tour_2

        # Relocation
        elif neighbor_order[neighbor_str] == 5:
          sub_tour[__tour2].insert(insert_position + 1, sub_tour[__tour1][customer])
          del sub_tour[__tour1][customer]

        neighbor_str = 0
        nb_no_imp = 0
      else:
        nb_no_imp += 1

        if nb_no_imp > len(neighbor_order):
          stop = True
        else:
          if neighbor_str >= len(neighbor_order) - 1:
            neighbor_str = 0
            stop = False
          else:
            neighbor_str += 1
