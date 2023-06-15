from flask import render_template, request, jsonify

from src.core.algorithms.TSP.bellman_held_karp_algorithm import BellmanHeldKarpAlgorithm
from src.core.algorithms.TSP.brute_force import BruteForceAlgorithm
from src.core.algorithms.TSP.simulated_annealing import SimulatedAnnealingAlgorithm
from src.core.utils.graph_visualization import GraphVisualization
from src.core.utils.problem_reader import ProblemReader
from src.core.utils.utilities import Utilities
from src.web.app import app

ALGORITHMS_MAP = {
  'bellman': BellmanHeldKarpAlgorithm,
  'brute-force': BruteForceAlgorithm,
  'simulated-annealing': SimulatedAnnealingAlgorithm,
}


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve_tsp():
  """ Prepare data for VRP solvers and return solution """
  problem = ProblemReader.read_tsp_problem(matrix=request.json['points'])
  algorithm = ALGORITHMS_MAP.get(request.json.get('algorithm'),
                                 SimulatedAnnealingAlgorithm)

  result = algorithm.run(problem)

  # Visualize and save graph image to ./data/img/graph.png
  png = GraphVisualization(problem, result.path).get_encoded_png(add_weight_labels=True,
                                                                 save_file=True)

  return jsonify({
    'path': Utilities.path_to_string(result.path),
    'length': result.length,
    'execution_report': {
      'algorithm': result.algorithm,
      'execution_time': result.execution_time
    },
    'image': png
  })
