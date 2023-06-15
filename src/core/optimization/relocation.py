""" Route improvements. Inter Relocation """
from src.core.models.problem import Problem
from src.core.utils.utilities import Utilities


def relocate(tour1, tour2, problem: Problem):
  best_imp = 0
  cust, position = -1, -1

  for i in range(1, len(tour1) - 1):
    if (problem.get_customer_by_id(tour1[i]).demand +
            problem.get_total_demand_for(tour2) <= problem.vehicle_capacity):

      for j in range(len(tour2) - 1):
        new_tour2 = tour2[:j + 1] + [tour1[i]] + tour2[j + 1:]

        time_check_relocate = Utilities.time_checker(new_tour2, problem)
        if time_check_relocate:
          tour1_imp = (problem.matrix[tour1[i - 1]][tour1[i]] +
                       problem.matrix[tour1[i]][tour1[i + 1]] -
                       problem.matrix[tour1[i - 1]][tour1[i + 1]])
          tour2_inc = (problem.matrix[tour2[j]][tour1[i]] +
                       problem.matrix[tour1[i]][tour2[j + 1]] -
                       problem.matrix[tour2[j]][tour2[j + 1]])

          if (tour2_inc - tour1_imp) < best_imp:
            best_imp = tour2_inc - tour1_imp
            cust = i
            position = j

  return cust, position, best_imp


def relocate_search(sub_tour, problem: Problem):
  best_imp = 0
  t1, t2 = -1, -1
  customer, position = -1, -1

  for i in range(len(sub_tour)):
    for j in range(len(sub_tour)):
      if i != j:
        [cust, pos, imp] = relocate(sub_tour[i], sub_tour[j], problem)

        if imp < best_imp:
          t1 = i
          t2 = j
          customer = cust
          position = pos
          best_imp = imp

  return t1, t2, customer, position, best_imp
