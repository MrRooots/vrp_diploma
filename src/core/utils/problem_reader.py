from __future__ import annotations

import ast
import os

import numpy as np

from src.core.models.customer import Customer
from src.core.models.depot import Depot
from src.core.models.graph import Graph
from src.core.models.problem import Problem
from src.core.models.tsp_problem import TSPProblem


class ProblemReader:
  """
  Problem reader.
  Read problem content and convert to specific format.
  """

  @staticmethod
  def read_tsp_problem(problem: str = None,
                       matrix: list[list[float]] | None = None) -> TSPProblem:
    """ Read TSP problem file or adjacency matrix. """
    problem_name, layout = problem, None

    if problem is not None:
      problem_file = f'data/input/{problem}'

      with open(problem_file, 'r') as file:
        matrix = [
          [float(v) if v != '0' else None for v in line.split()]
          for line in file
        ]

      print(f'Loaded "{problem_file}" problem file')
    else:
      problem_name = 'User Defined'

    layout_file = f'data/input/layouts/layout_{len(matrix)}.in'

    if os.path.isfile(layout_file):
      with open(layout_file, 'r') as f:
        layout = ast.literal_eval(f.readline())

    return TSPProblem(name=problem_name, graph=Graph(matrix, layout))

  @staticmethod
  def read_problem_file(problem: str = 'c101',
                        customers_count: int = None) -> Problem:
    """
    Read data from given problem file. Special format required

    References
      [1]: Format description http://w.cba.neu.edu/~msolomon/problems.htm
    """
    folder = problem[0:2]
    problem_file = f'data/input/problems/{folder}/' + problem + '.in' if problem[-3:] != '.in' else problem

    customer_count = 0
    instance_name: str = ''
    max_vehicle_number: int = 0
    vehicle_capacity: float = 0
    depart: Depot | None = None
    customers: list[Customer] = []

    with open(problem_file, 'r') as file_object:
      for line_num, line in enumerate(file_object, start=1):
        if line_num in [2, 3, 4, 6, 7, 8, 9]:
          pass
        elif line_num == 1:
          instance_name = line.strip()
        elif line_num == 5:
          values = line.strip().split()
          max_vehicle_number = int(values[0])
          vehicle_capacity = float(values[1])
        elif line_num == 10:
          values = line.strip().split()
          depart = Depot(*map(float, values))
        else:
          values = line.strip().split()
          customers.append(Customer(*map(float, values)))
          if customers_count is not None:
            customer_count += 1
            if customer_count == customers_count:
              break

    print(f'Loaded "{problem_file}" problem file')

    return Problem(name=instance_name,
                   max_vehicle=max_vehicle_number,
                   vehicle_capacity=vehicle_capacity,
                   depot=depart,
                   customers=customers,
                   graph=Graph(matrix=[
                     [
                       c1.calculate_distance_to(c2)
                       for c1 in [depart, *customers]
                     ] for c2 in [depart, *customers]
                   ]))
