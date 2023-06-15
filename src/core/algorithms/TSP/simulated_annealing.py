from math import inf
from random import sample
from timeit import default_timer

import numpy as np

from src.core.algorithms.TSP.pertubation_schemes import neighborhood_gen
from src.core.interfaces.i_tsp_algorithm import ITSPAlgorithm
from src.core.models.graph import Graph
from src.core.models.result import ResultModel
from src.core.models.tsp_problem import TSPProblem
from src.core.utils.decorators import Decorators
from src.core.utils.utilities import Utilities

Matrix = list[list[float]]

MAX_NON_IMPROVEMENTS = 3
MAX_INNER_ITERATIONS_MULTIPLIER = 10


class SimulatedAnnealingAlgorithm(ITSPAlgorithm):
  """
  References
    [1] Dréo, Johann, et al. Metaheuristics for hard optimization: methods and
    case studies. Springer Science & Business Media, 2006.
  """

  @staticmethod
  def _initial_temperature(graph: Graph,
                           x: list[int],
                           fx: float,
                           perturbation_scheme: str) -> float:
    """
    Compute initial temperature.

    Instead of relying on problem-dependent parameters, this function estimates
    the temperature using the suggestion in [1].

    Notes
      - Steps:
        1. Generate 100 disturbances at random from T0, and evaluate the mean
        objective value differences dfx_mean = mean(fn - fx);

        2. Choose tau0 = 0.5 as assumed quality of initial solution (assuming
        a bad one), and deduce T0 from exp(-fx_mean/T0) = tau0, that is,
        T0 = -fx_mean/ln(tau0)
    """

    # Step 1
    dfx_list = []
    for _ in range(100):
      xn = SimulatedAnnealingAlgorithm._perturbation(x, perturbation_scheme)
      fn = Utilities.permutation_distance(graph.safe_matrix, xn)
      dfx_list.append(fn - fx)

    dfx_mean = np.abs(np.mean(dfx_list))

    # Step 2
    tau0 = 0.5
    return -dfx_mean / np.log(tau0)

  @staticmethod
  def _perturbation(x: list[int], perturbation_scheme: str):
    """
    Generate a random neighbor of a current solution ``x``
    """
    return next(neighborhood_gen[perturbation_scheme](x))

  @staticmethod
  def _acceptance_rule(fx: float, fn: float, temp: float) -> bool:
    """
    Metropolis acceptance rule.
    Used for select sample from distribution
    """

    dfx = fn - fx
    return (dfx < 0) or (
            (dfx > 0) and (np.random.rand() <= np.exp(-(fn - fx) / temp))
    )

  @staticmethod
  def get_initial_solution(matrix: Matrix,
                           x0: list = None) -> tuple[list[int], float]:
    """
    Return initial solution and its objective value

    x0 - Permutation with initial solution.
    If `x0` was provided, it is the same list

    fx0 - Objective value of x0
    """

    if not x0:
      n = len(matrix)
      x0 = [0] + sample(range(1, n), n - 1)

    fx0 = Utilities.permutation_distance(matrix, x0)
    return x0, fx0

  @staticmethod
  @Decorators.convert_to_result_model
  def run(problem: TSPProblem,
          x0: list[int] = None,
          perturbation_scheme: str = "two_opt",
          alpha: float = 0.9,
          time_limit: float = None,
          log_steps: bool = False,
          **kwargs):
    x, fx = SimulatedAnnealingAlgorithm.get_initial_solution(problem.graph.safe_matrix, x0)

    temp = SimulatedAnnealingAlgorithm._initial_temperature(problem.graph,
                                                            x,
                                                            fx,
                                                            perturbation_scheme)
    time_limit = time_limit or inf

    n = len(x)
    k_inner_min = n
    k_inner_max = MAX_INNER_ITERATIONS_MULTIPLIER * n
    k_without_improvements = 0  # number of inner loops without improvement

    tic = default_timer()
    stop_early = False

    while (k_without_improvements < MAX_NON_IMPROVEMENTS) and (not stop_early):
      k_accepted = 0  # number of accepted perturbations

      for k in range(k_inner_max):
        if default_timer() - tic > time_limit:
          print('[WARNING]: Stopping early due to time constraints')
          stop_early = True
          break

        xn = SimulatedAnnealingAlgorithm._perturbation(x, perturbation_scheme)
        fn = Utilities.permutation_distance(problem.graph.safe_matrix, xn)

        if SimulatedAnnealingAlgorithm._acceptance_rule(fx, fn, temp):
          x, fx = xn, fn
          k_accepted += 1
          k_without_improvements = 0

        if log_steps:
          print(
            f"Temperature {temp}. Current value: {fx} "
            f"k: {k + 1}/{k_inner_max} "
            f"k_accepted: {k_accepted}/{k_inner_min} "
            f"k_without_improvements: {k_without_improvements}"
          )

        if k_accepted >= k_inner_min:
          break

      temp *= alpha  # temperature update
      k_without_improvements += k_accepted == 0

    return [x], [fx]
