from typing import Type

from src.core.interfaces.i_vrptw_algorithm import IVRPTWAlgorithm
from src.core.models.result import ResultModel


class ITSPSolver:
  """
  Vehicle routing problem with time windows algorithms interface.
  """

  def solve_vrp(self,
                solver: Type[IVRPTWAlgorithm],
                report: bool = False) -> ResultModel:
    """ Solve VRPTW problem for given graph """
