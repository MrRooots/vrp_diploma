import time
from src.core.models.result import ResultModel


class Decorators:
  @staticmethod
  def timeit(func: callable):
    """ Simplest timer decorator """

    def wrapper(*args, **kwargs):
      start = time.time()
      result = func(*args, **kwargs)
      print(f'Execution time of {func.__qualname__}: {round((time.time() - start) * 1000, 8)} ms')

      return result

    return wrapper

  @staticmethod
  def convert_to_result_model(func: callable) -> callable:
    """ Timer decorator that convert function result to `ResultModel` """

    def wrapper(*args, **kwargs) -> ResultModel:
      start = time.time()
      result = func(*args, **kwargs)

      return ResultModel(*result,
                         execution_time=round((time.time() - start) * 1000, 8),
                         algorith=func.__qualname__)

    return wrapper
