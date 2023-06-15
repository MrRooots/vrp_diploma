import copy
import time

import numpy as np

from src.core.algorithms.VRPTW.tour_shaker import TourShaker
from src.core.algorithms.VRPTW.variable_neighborhood_search import VariableNeighborhoodSearch
from src.core.models.problem import Problem
from src.core.models.result import ResultModel
from src.core.utils.utilities import Utilities


class SolutionTuner:
  @staticmethod
  def tune_solution(initial_solution: ResultModel, problem: Problem):
    rnd = np.random
    rnd.seed(0)

    DIST, NO_VEHICLE, RUN_TIME = [], [], []
    iteration_count = 2
    sub_tour_vns = None

    # MAIN CODE
    for counter in range(iteration_count):
      sub_tour_vns = copy.deepcopy(initial_solution.path)
      shaking_neighbor = [0, 1, 2, 3, 4, 5]
      time_start = time.time()

      no_improvements, n, stop = 0, 0, False

      while not stop:
        sub_tour_shaking = TourShaker.shake(tours=sub_tour_vns,
                                            problem=problem,
                                            neighbours=shaking_neighbor[n])

        VariableNeighborhoodSearch.optimize_tour(sub_tour=sub_tour_shaking,
                                                 problem=problem,
                                                 neighbours=shaking_neighbor)

        sub_tour_shaking_demand = Utilities.total_distance(sub_tour_shaking, problem)
        sub_tour_vns_demand = Utilities.total_distance(sub_tour_vns, problem)

        if sub_tour_shaking_demand < sub_tour_vns_demand:
          sub_tour_vns = copy.deepcopy(sub_tour_shaking)
          n = 0
          no_improvements = 0
        else:
          no_improvements += 1

          if no_improvements > len(shaking_neighbor):
            stop = True
          else:
            if n >= len(shaking_neighbor) - 1:
              n = 0
              stop = False
            else:
              n += 1
              stop = False
        sub_tour_vns = [sub_tour_vns[i] for i in range(len(sub_tour_vns))
                        if len(sub_tour_vns[i]) > 2]  # Remove empty tour

      time_end = time.time()

      dist = Utilities.total_distance(sub_tour_vns, problem)
      no_veh = len(sub_tour_vns)
      time_exe = time_end - time_start

      DIST.append(dist)
      NO_VEHICLE.append(no_veh)
      RUN_TIME.append(time_exe)

      print('[FOR LOOP]:', counter + 1, dist, no_veh, time_exe)
      print(f'[FOR LOOP]: {sub_tour_vns}')

    # print('\n', min(NO_VEHICLE), np.mean(NO_VEHICLE), np.std(NO_VEHICLE))
    # print(min(DIST), np.mean(DIST), np.std(DIST), np.mean(RUN_TIME))
    print("====================")
    print(f'Final tour: {sub_tour_vns}')

    return sub_tour_vns
