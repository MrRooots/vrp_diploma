from src.core.models.problem import Problem


class IOptimizer:
  """
  Optimizer base class.

  Note
    Oriented to implementation of
    - 2-opr
    - or-opt
    - 2-opt *
  """

  @staticmethod
  def __move(*args) -> tuple:
    """ Optimizer move """

  @staticmethod
  def improve(tours: list[list[int]], problem: Problem, *args) -> tuple:
    """ Attempt to improve all sub-tours for given `tours` """
