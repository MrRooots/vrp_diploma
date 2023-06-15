""" Route improvements. 2-opt* """
from src.core.models.problem import Problem
from src.core.utils.utilities import Utilities


def two_optstar(tour1: list[int], tour2: list[int], problem: Problem):
  best_imp = 0
  position1 = -1
  position2 = -1

  for i in range(0, len(tour1) - 1):
    for j in range(0, len(tour2) - 1):
      new_tour1 = tour1[:i + 1] + tour2[j + 1:]
      new_tour2 = tour2[:j + 1] + tour1[i + 1:]
      tour1_new_demand = problem.get_total_demand_for(new_tour1)
      tour2_new_demand = problem.get_total_demand_for(new_tour2)

      if (tour1_new_demand <= problem.vehicle_capacity and
              tour2_new_demand <= problem.vehicle_capacity):

        time_check_2opts1 = Utilities.time_checker(new_tour1, problem)
        time_check_2opts2 = Utilities.time_checker(new_tour2, problem)

        if time_check_2opts1 and time_check_2opts2:
          twoopts_cost = round(problem.matrix[tour1[i]][tour2[j + 1]] +
                               problem.matrix[tour2[j]][tour1[i + 1]] -
                               problem.matrix[tour1[i]][tour1[i + 1]] -
                               problem.matrix[tour2[j]][tour2[j + 1]], 10)

          if twoopts_cost < best_imp:
            best_imp = twoopts_cost
            position1 = i
            position2 = j

  return position1, position2, best_imp


def two_optstar_search(sub_tour, problem: Problem):
  best_imp = 0
  t1 = -1
  t2 = -1
  position_1 = -1
  position_2 = -1

  for i in range(len(sub_tour) - 1):
    for j in range(i + 1, len(sub_tour)):
      [p1, p2, imp] = two_optstar(sub_tour[i], sub_tour[j], problem)

      if imp < best_imp:
        t1 = i
        t2 = j
        position_1 = p1
        position_2 = p2
        best_imp = imp

  return t1, t2, position_1, position_2, best_imp
