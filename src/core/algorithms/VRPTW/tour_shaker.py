import copy
import time
import random

from src.core.models.problem import Problem
from src.core.utils.utilities import Utilities


class TourShaker:
  """
  Tour shaker implementation.
  """

  @staticmethod
  def two_opt_shaker(n: int,
                     sub_tour: list[list[int]],
                     shaking_start: float,
                     problem: Problem):
    """"""
    while True:
      while True:
        tour = random.randint(0, n)
        if len(sub_tour[tour]) >= 5:
          break

      position_1 = random.randint(0, len(sub_tour[tour]) - 4)
      position_2 = random.randint(position_1 + 2, len(sub_tour[tour]) - 2)

      new_tour = (sub_tour[tour][0:position_1 + 1] +
                  sub_tour[tour][position_1 + 1:position_2 + 1][::-1] +
                  sub_tour[tour][position_2 + 1:])
      time_check = Utilities.time_checker(new_tour, problem)

      shaking_end = time.time()

      if time_check:
        sub_tour[tour] = new_tour
        break
      elif shaking_end - shaking_start > 0.5:
        break

  @staticmethod
  def or_opt_shaker(n: int,
                    k: int,
                    sub_tour: list[list[int]],
                    shaking_start: float,
                    problem: Problem):
    """"""
    while True:
      while True:
        tour = random.randint(0, n)
        if len(sub_tour[tour]) >= k + 3:
          break

      position_1 = random.randint(0, len(sub_tour[tour]) - k - 2)
      position_2 = position_1 + k
      position_3 = random.randint(0, len(sub_tour[tour]) - 2)

      while position_1 <= position_3 <= position_2:
        position_3 = random.randint(0, len(sub_tour[tour]) - 2)

      if position_3 < position_1:
        new_tour = (sub_tour[tour][:position_3 + 1] +
                    sub_tour[tour][position_1 + 1:position_2 + 1] +
                    sub_tour[tour][position_3 + 1:position_1 + 1] +
                    sub_tour[tour][position_2 + 1:])
      else:
        new_tour = (sub_tour[tour][:position_1 + 1] +
                    sub_tour[tour][position_2 + 1:position_3 + 1] +
                    sub_tour[tour][position_1 + 1:position_2 + 1] +
                    sub_tour[tour][position_3 + 1:])

      time_check = Utilities.time_checker(new_tour, problem)

      shaking_end = time.time()

      if time_check:
        sub_tour[tour] = new_tour
        break
      elif shaking_end - shaking_start > 0.5:
        break

  @staticmethod
  def two_opt_star_shaker(n: int,
                          sub_tour: list[list[int]],
                          shaking_start: float,
                          problem: Problem):
    """"""
    while True:
      tour_1 = random.randint(0, n - 1)
      tour_2 = random.randint(tour_1 + 1, n)
      position_1 = random.randint(1, len(sub_tour[tour_1]) - 2)
      position_2 = random.randint(1, len(sub_tour[tour_2]) - 2)

      new_tour_1 = sub_tour[tour_1][:position_1 + 1] + sub_tour[tour_2][position_2 + 1:]
      new_tour_2 = sub_tour[tour_2][:position_2 + 1] + sub_tour[tour_1][position_1 + 1:]

      time_check1 = Utilities.time_checker(new_tour_1, problem)
      time_check2 = Utilities.time_checker(new_tour_2, problem)
      new_tour1_demand = sum(i.demand for i in problem.get_customers_by_id(new_tour_1))
      new_tour2_demand = sum(i.demand for i in problem.get_customers_by_id(new_tour_2))

      shaking_end = time.time()

      if (time_check1 and time_check2 and
              new_tour1_demand <= problem.vehicle_capacity and
              new_tour2_demand <= problem.vehicle_capacity):
        sub_tour[tour_1] = new_tour_1
        sub_tour[tour_2] = new_tour_2
        break
      elif shaking_end - shaking_start > 0.5:
        break

  @staticmethod
  def relocation_shaker(n: int,
                        sub_tour: list[list[int]],
                        shaking_start: float,
                        problem: Problem):
    """"""
    while True:
      first_tour = random.randint(0, n)
      second_tour = random.randint(0, n)

      while first_tour == second_tour:
        second_tour = random.randint(0, n)

      customer = random.randint(1, len(sub_tour[first_tour]) - 2)
      insert_pos = random.randint(0, len(sub_tour[second_tour]) - 2)

      new_tour = (sub_tour[second_tour][:insert_pos + 1] +
                  [sub_tour[first_tour][customer]] +
                  sub_tour[second_tour][insert_pos + 1:])

      time_passed = Utilities.time_checker(new_tour, problem)
      tour2_demand = (problem.get_customer_by_id(sub_tour[first_tour][customer]).demand +
                      problem.get_total_demand_for(sub_tour[second_tour]))

      shaking_end = time.time()

      if time_passed and tour2_demand <= problem.vehicle_capacity:
        sub_tour[second_tour].insert(insert_pos + 1, sub_tour[first_tour][customer])
        del sub_tour[first_tour][customer]
        break
      elif shaking_end - shaking_start > 0.5:
        break

  @staticmethod
  def shake(tours: list[list[int]], problem: Problem, neighbours):
    n = len(tours) - 1
    sub_tour = copy.deepcopy(tours)
    shaking_start = time.time()

    # 2-opt
    if neighbours == 0:
      TourShaker.two_opt_shaker(n, sub_tour, shaking_start, problem)

    # Or-opt 1, 2, 3
    elif neighbours in (1, 2, 3):
      k = neighbours
      TourShaker.or_opt_shaker(n, k, sub_tour, shaking_start, problem)

    # 2-optstar
    elif neighbours == 4 and n > 0:
      TourShaker.two_opt_star_shaker(n, sub_tour, shaking_start, problem)

    # Relocation
    elif neighbours == 5 and n > 0:
      TourShaker.relocation_shaker(n, sub_tour, shaking_start, problem)

    return sub_tour
