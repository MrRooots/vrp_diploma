from matplotlib import pyplot as plt

from src.core.models.problem import Problem


class Plotter:
  """
  Solution visualizer.
  """

  @staticmethod
  def visualize_solution(tour: list[list[int]],
                         problem: Problem,
                         title: str) -> None:
    """ Visualize given `tour` that contains `customer_count` nodes """
    x, y = problem.get_coords

    plt.style.use('dark_background')
    plt.figure(figsize=(16, 16), dpi=50)
    plt.plot(x[0], y[0], 'r+')
    plt.scatter(x[1:], y[1:], s=5, c='k', marker=',')

    for i in range(1, problem.customers_count + 1):
      plt.annotate(i, (x[i] + 0.2, y[i] + 0.2), size=8)

    for i in range(len(tour)):
      plt.plot([x[j] for j in tour[i]], [y[j] for j in tour[i]])

    plt.title(title)
    plt.show()
