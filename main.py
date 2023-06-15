from src.core.algorithms.TSP.bellman_held_karp_algorithm import BellmanHeldKarpAlgorithm
from src.core.algorithms.TSP.brute_force import BruteForceAlgorithm
from src.core.algorithms.TSP.simulated_annealing import SimulatedAnnealingAlgorithm
from src.core.algorithms.VRPTW.solomon_i1 import SolomonI1
from src.core.algorithms.VRPTW.solution_tuner import SolutionTuner
from src.core.models.result import ResultModel

from src.core.utils.graph_visualization import GraphVisualization
from src.core.utils.plotter import Plotter
from src.core.utils.problem_reader import ProblemReader
from src.core.utils.utilities import Utilities
from src.web.server import run_server


def main_tsp(problem_name: str) -> None:
  """ Solve TSP problem """
  problem = ProblemReader.read_tsp_problem(problem=problem_name)

  for solution_method in (
          BellmanHeldKarpAlgorithm,
          BruteForceAlgorithm,
          SimulatedAnnealingAlgorithm,
  ):
    result = solution_method.run(problem, source=0)
    print(result.get_complete_report)

    # GraphVisualization(problem, result.path).visualize(add_weight_labels=True)


def main_vrp(problem_name: str = 'c101', customers_count: int = 25) -> None:
  """ Solve VRPTW problem """
  # Read problem file
  problem = ProblemReader.read_problem_file(problem_name, customers_count)

  # Get initial solution
  unrouted_customers = list(range(1, customers_count + 1))
  initial_solution: ResultModel = SolomonI1.run(unrouted_customers, problem=problem)
  print(initial_solution.get_complete_report)

  # [MAGIC GOES HERE]: Fine tuning
  Plotter.visualize_solution(initial_solution.path, problem, 'Initial solution')
  print('0', Utilities.total_distance(initial_solution.path, problem), len(initial_solution.path))

  tuned_solution = SolutionTuner.tune_solution(initial_solution=initial_solution,
                                               problem=problem)

  if tuned_solution:
    print(f'Tuned solution: {tuned_solution}')
    Plotter.visualize_solution(tuned_solution, problem, 'Tuned solution')
    print(Utilities.total_distance(tuned_solution, problem))
  else:
    'Failed to tune solution'


def start_http_server() -> None:
  """ Start socket server that provides simple algorithms interface """
  # SocketServer().run()
  run_server()


if __name__ == '__main__':
  # if '--server' in sys.argv:
  # start_http_server()
  # else:
  # main_tsp('5.in')
  main_vrp('c106', 50)
  # for filename in os.listdir('./data/input'):
  #   main(filename)
