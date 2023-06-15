from src.core.utils.utilities import Utilities


class ResultModel:
  """
  Algorithms result model
  """

  # Calculated shortest path
  path: list[list[int]]

  # Calculated minimal path cost
  length: list[float]

  # Execution time [ms]
  execution_time: float

  # Executed algorithm name
  algorithm: str

  def __init__(self,
               path: list[list[int]],
               length: list[float],
               execution_time: float,
               algorith: str) -> None:
    self.path = path
    self.length = length
    self.execution_time = execution_time
    self.algorithm = algorith

  @property
  def get_path_report(self) -> str:
    """ Generate path report """
    if len(self.path) > 1:
      template = 'Calculated shortest paths:\n'

      for i, (path, length) in enumerate(zip(self.path, self.length)):
        template += f'\tPath {i + 1} is: {Utilities.path_to_string(path)} with length: {length}\n'

      return template

    return f'Shortest path is: {Utilities.path_to_string(self.path[0])} with length: {self.length[0]}'

  @property
  def get_time_report(self) -> str:
    """ Generate execution report """
    return f'Execution time of {self.algorithm}: {self.execution_time} ms'

  @property
  def get_complete_report(self) -> str:
    """ Generate complete report with the shortest path and execution time """
    return self.get_path_report + '\n' + self.get_time_report
