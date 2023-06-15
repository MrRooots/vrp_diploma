from src.core.models.problem import Problem

Matrix = list[list[float]]


class IUtilities:
  @staticmethod
  def permutation_distance(matrix: Matrix,
                           permutation: list[int]) -> float:
    """
    Compute the total route distance of a given permutation

    Suppose the permutation [0, 1, 2, 3], with four nodes. The total distance
    of this path will be from 0 to 1, 1 to 2, 2 to 3, and 3 back to 0.
    """

  @staticmethod
  def time_checker(tour: list[int], problem: Problem) -> bool:
    """
    Функция time_checker выполняет проверку, удовлетворяют ли все точки маршрута
    временным ограничениям.

    Функция начинает с инициализации времени (time) и счетчика равными нулю.
    Затем она выполняет цикл по всем точкам маршрута, начиная с индекса 1.
    Для каждой точки маршрута, функция вычисляет время, когда она будет достигнута.
    Это время определяется как максимум между временем, когда
    предыдущая точка становится доступной (ready_time[tour[i - 1]]),
    временем обслуживания предыдущей точки (service_time[tour[i - 1]]),
    и временем путешествия между предыдущей точкой и текущей точкой (travel_time[tour[i - 1]][tour[i]]).

    Затем функция проверяет, удовлетворяет ли время доставки текущей точки
    временному окну (due_time[tour[i]]).
    Если это так, увеличивается счетчик counter.
    Если время доставки превышает временное окно, цикл прерывается.

    Таким образом, функция time_checker проверяет, удовлетворяют ли
    заданные точки маршрута временным ограничениям доставки
    """

  @staticmethod
  def begin_time(tour: list[int], problem: Problem) -> list[int]:
    """
    Цель функции состоит в том, чтобы вычислить время начала обслуживания
    в каждой точке маршрута.

    Функция возвращает список begin_service_time, содержащий время
    начала обслуживания для каждой точки маршрута.
    """


class Utilities(IUtilities):
  """
  Some useful utilities_1
  """

  @staticmethod
  def path_to_string(path: list[int], sep: str = ' -> ') -> str:
    """ Convert given path to string: '1 -> 2 -> 3' """
    return sep.join(map(str, path))

  @staticmethod
  def permutation_distance(matrix: Matrix, permutation: list[int]) -> float:
    distance, n = 0.0, len(permutation)

    for i in range(n):
      ind1 = permutation[i]
      ind2 = permutation[(i + 1) % n]
      distance += matrix[ind1][ind2]

    return distance

  @staticmethod
  def time_checker(tour: list[int], problem: Problem) -> bool:
    time, counter = 0, 0

    for i in range(1, len(tour)):
      prev_customer, curr_customer = problem.get_customers_by_id([tour[i - 1],
                                                                  tour[i]])
      time = (max(time, prev_customer.ready_time) +
              prev_customer.service_time +
              problem.matrix[tour[i - 1]][tour[i]])

      if time <= curr_customer.due_time:
        counter += 1
      else:
        break

    return counter == len(tour) - 1

  @staticmethod
  def begin_time(tour: list[int], problem: Problem) -> list[int]:
    begin_service_time, time = [0], 0

    for i in range(1, len(tour)):
      prev_customer, curr_customer = problem.get_customers_by_id([tour[i - 1], tour[i]])

      time = (max(time, prev_customer.ready_time)
              + prev_customer.service_time
              + problem.matrix[tour[i - 1]][tour[i]])

      begin = max(time, curr_customer.ready_time)
      begin_service_time.append(begin)

    return begin_service_time

  @staticmethod
  def total_distance(tours, problem: Problem) -> float:
    total_distance = 0

    for tour in tours:
      tour_distance = 0

      for i in range(len(tour) - 1):
        tour_distance += problem.matrix[tour[i]][tour[i + 1]]

      total_distance += tour_distance

    return total_distance
