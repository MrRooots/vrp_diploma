from flask import render_template, request, jsonify

from src.core.algorithms.TSP.simulated_annealing import SimulatedAnnealingAlgorithm
from src.core.structures.graph import Graph
from src.core.structures.vrp_solver import VRPSolver
from src.core.utils.graph_visualization import GraphVisualization
from src.core.utils.utilities import Utilities
from src.web.app import app


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve_vrp():
  """ Prepare data for VRP solvers and return solution """
  graph = Graph.from_adjacency_matrix(request.json['points'])
  source = request.json.get('source') or 0
  destination = request.json.get('source') or graph.vertex_count - 1
  solver = VRPSolver(graph)
  solver.set_source_node(source)
  solver.set_destination_node(destination)

  result = solver.solve_vrp(SimulatedAnnealingAlgorithm)
  print(result.get_complete_report)

  # Visualize and save graph image to ./data/img/graph.png
  png = GraphVisualization(graph, result.path).get_encoded_png(add_weight_labels=True,
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
