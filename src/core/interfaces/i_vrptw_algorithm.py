from src.core.models.problem import Problem


class IVRPTWAlgorithm:
  """
  Vehicle routing problem with time windows algorithms base class.
  """

  @staticmethod
  def run(problem: Problem,
          **kwargs) -> tuple[list[int], float]:
    """ Start pure algorithm for given VRPTW `problem` """
