from src.core.algorithms.TSP.simulated_annealing import SimulatedAnnealingAlgorithm
from src.core.algorithms.TSP.bellman_held_karp_algorithm import BellmanHeldKarpAlgorithm
from src.core.algorithms.TSP.brute_force import BruteForceAlgorithm
from src.core.utils.graph_generator import GraphGenerator
from src.core.utils.graph_visualization import GraphVisualization
from src.core.utils.report_manager import ReportManager

graph = GraphGenerator.from_file('extreme_150.in')
# GraphVisualization(graph).visualize(add_weight_labels=True)

# path, distances = BruteForceAlgorithm.run(graph)
# ReportManager.make_report_from_complete_data(path, distances)

# path, distances = BellmanHeldKarpAlgorithm.run(graph)
# ReportManager.make_report_from_complete_data(path, distances)

a, b = SimulatedAnnealingAlgorithm.run(graph)
ReportManager.make_report_from_complete_data(a, b)
