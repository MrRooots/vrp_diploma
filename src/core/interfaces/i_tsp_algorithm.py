from src.core.models.result import ResultModel
from src.core.models.tsp_problem import TSPProblem


class ITSPAlgorithm:
  """
  Travelling salesman problem algorithms base class.
  """

  @staticmethod
  def run(problem: TSPProblem,
          **kwargs) -> ResultModel:
    """ Start pure algorithm for given TSP `problem` """
