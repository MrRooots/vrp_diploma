import os
import sys

from lib.src.algoritms.dijkstra_with_node_filtering import DijkstraWithNodeFiltering
from lib.src.structures.vrp_solver import VRPSolver
from lib.src.utils.graph_generator import GraphGenerator
from lib.src.utils.graph_visualization import GraphVisualization
from lib.web.socket_server import SocketServer


def main(filename: str) -> None:
  """ Solve VRP problem """
  graph = GraphGenerator.from_file(filename)

  GraphVisualization(graph).visualize(add_weight_labels=True)

  solver = VRPSolver(graph, source_node=0)

  for solution_method in (DijkstraWithNodeFiltering,):
    solver.solve_vrp(solution_method, report=True)


def start_http_server() -> None:
  """ Start socket server that provides simple algorithms interface """
  SocketServer().run()


if __name__ == '__main__':
  if '--http-server' in sys.argv:
    start_http_server()
  else:
    for filename in os.listdir('./data'):
      main(filename)
