from typing import Type

from src.core.interfaces.i_tsp_algorithm import ITSPAlgorithm
from src.core.models.result import ResultModel


class ITSPSolver:
  """
  Travelling salesman problem algorithms interface.
  """

  def solve_tsp(self,
                solver: Type[ITSPAlgorithm],
                report: bool = False) -> ResultModel:
    """ Solve TSP problem for given graph """
