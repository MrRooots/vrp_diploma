import json

from lib.src.algoritms.dijkstra_with_node_filtering import DijkstraWithNodeFiltering
from lib.src.structures.vrp_solver import VRPSolver
from lib.src.utils.graph_generator import GraphGenerator


class Views:
  @staticmethod
  def _render_template(template: str, static: bool = False) -> str:
    """ Read given template file """
    filename = f'{"templates" if not static else "static"}/{template}'

    with open(filename) as template:
      return template.read()

  @staticmethod
  def index() -> str:
    """ Render index page """
    return Views._render_template('index.html')

  @staticmethod
  def not_found() -> str:
    """ Render 404 page """
    return Views._render_template('404.html')

  @staticmethod
  def internal_server_error() -> str:
    """ Render 500 page """
    return Views._render_template('500.html')

  @staticmethod
  def load_scripts() -> str:
    return Views._render_template('scripts.js', static=True)

  @staticmethod
  def load_styles() -> str:
    return Views._render_template('style.css', static=True)

  @staticmethod
  def solve_vrp(data: dict[str, list[list[float]]]):
    graph = GraphGenerator.from_adjacency_matrix(data['points'])
    solver = VRPSolver(graph)
    path, length = solver.solve_vrp(DijkstraWithNodeFiltering)

    return json.dumps({
      'path': path,
      'length': length
    })
