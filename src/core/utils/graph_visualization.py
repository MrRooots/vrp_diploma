import base64
from io import BytesIO

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from src.core.models.graph import Graph
from src.core.models.tsp_problem import TSPProblem

EDGE_COLOR = '#d3d3d34D'
EDGE_ACCENT_COLOR = '#f08080'
NODE_COLOR = EDGE_COLOR
NODE_ACCENT_COLOR = EDGE_ACCENT_COLOR
LEGEND_ELEMENTS = [
  Line2D([0], [0], color=EDGE_COLOR, linewidth=5, label='Unused path', markersize=15),
  Line2D([0], [0], color=EDGE_ACCENT_COLOR, linewidth=5, label='Selected path', markersize=15),
]


class GraphVisualization:
  """
  Graph visualization utility.
  """

  """ Graph draw potions """
  options = {'with_labels': True,
             'edge_color': [EDGE_COLOR],
             'node_color': [NODE_COLOR],
             'node_size': 600,
             'font_color': 'black',
             'width': 2}

  graph: Graph = None
  network_graph: nx.Graph | nx.DiGraph = None

  def __init__(self, problem: TSPProblem, path: list[list[int]] = None) -> None:
    self.graph = problem.graph
    self.network_graph = nx.Graph() if self.graph.is_symmetric else nx.DiGraph()

    self.__prepare_network_graph()
    path = path[0]
    if path is not None:
      self.options['node_color'] = [
        NODE_ACCENT_COLOR if node in path else EDGE_COLOR
        for node in self.network_graph.nodes
      ]
      _path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
      self.options['edge_color'] = [
        EDGE_ACCENT_COLOR if edge in _path or edge[::-1] in _path else EDGE_COLOR
        for edge in self.network_graph.edges
      ]

  def __prepare_network_graph(self) -> None:
    """ Convert adjacency matrix to nx.Graph object """
    self.network_graph.add_nodes_from(range(self.graph.vertex_count))
    self.network_graph.add_weighted_edges_from([
      (i, j, weight)
      for i, row in enumerate(self.graph.matrix)
      for j, weight in enumerate(row)
      if weight is not None and i != j
    ])

  def _build_plot(self, add_weight_labels: float = False) -> None:
    if self.graph.layout is not None:
      layout = self.graph.layout
    else:
      layout = nx.spring_layout(self.network_graph)

    plt.figure(figsize=(10, 10), dpi=300)
    plt.title(f'Graph visualization for {self.graph.vertex_count} nodes')
    plt.legend(handles=LEGEND_ELEMENTS, loc='upper right')

    nx.draw(self.network_graph, layout, **self.options)

    if add_weight_labels:
      edge_labels = nx.get_edge_attributes(self.network_graph, 'weight')
      nx.draw_networkx_edge_labels(self.network_graph,
                                   layout,
                                   edge_labels=edge_labels)

  def get_encoded_png(self,
                      add_weight_labels: float = False,
                      filename: str = 'graph',
                      save_file: bool = False) -> str:
    """ Visualize current `graph` and return it as png """
    self._build_plot(add_weight_labels=add_weight_labels)

    buffer = BytesIO()
    path = f'./data/img/{filename}.png'

    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    if save_file:
      with open(path, 'wb') as file:
        file.write(buffer.read())

      buffer.seek(0)

    return base64.b64encode(buffer.read()).decode()

  def visualize(self, add_weight_labels: float = False) -> None:
    """ Visualize the current graph """
    self._build_plot(add_weight_labels)

    plt.show()
    plt.close()
