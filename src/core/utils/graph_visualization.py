import networkx as nx
import matplotlib.pyplot as plt

from src.core.structures.graph import Graph


class GraphVisualization:
  """
  Graph visualization.
  """

  """ Graph draw potions """
  options = {'with_labels': True,
             'edge_color': '#3DA3F5',
             'node_color': 'lightblue',
             'font_color': 'black',
             'width': 1.5}

  graph: Graph = None
  network_graph: nx.Graph | nx.DiGraph = None

  def __init__(self, graph: Graph) -> None:
    self.graph = graph
    self.network_graph = nx.Graph() if graph.is_symmetric else nx.DiGraph()

    self.__prepare_network_graph()

  def __add_weight_labels(self) -> dict[tuple[float, float], float]:
    num_nodes = len(self.graph.matrix)

    return {
      (i, j): self.graph.matrix[i][j]
      for i in range(num_nodes)
      for j in range(i + 1, num_nodes)
      if self.graph.matrix[i][j] > 0
    }

  def __prepare_network_graph(self) -> None:
    """ Convert adjacency matrix to nx.Graph object """
    num_nodes = len(self.graph.matrix)
    self.network_graph.add_nodes_from(range(num_nodes))
    # self.network_graph.add_weighted_edges_from([
    #   (i, j, self.graph.matrix[i][j])
    #   for i in range(num_nodes)
    #   for j in range(i + 1, num_nodes)
    #   if self.graph.matrix[i][j] is not None
    # ])
    self.network_graph.add_weighted_edges_from([
      (i, j, weight) if i != j else (i, j, 0)
      for i, row in enumerate(self.graph.matrix)
      for j, weight in enumerate(row) if weight is not None
    ])

  def visualize(self,
                add_weight_labels: float = False,
                show: bool = True) -> None:
    """ Visualize the current graph """
    if self.graph.layout is not None:
      layout = self.graph.layout
    else:
      layout = nx.spring_layout(self.network_graph)

    nx.draw(self.network_graph, layout, **self.options)

    if add_weight_labels:
      edge_labels = self.__add_weight_labels()
      nx.draw_networkx_edge_labels(self.network_graph,
                                   layout,
                                   edge_labels=edge_labels)

    plt.show() if show else plt.savefig('./data/img/graph.png', format='png')
    plt.close()
