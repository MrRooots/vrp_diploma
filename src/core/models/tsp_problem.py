from src.core.models.graph import Graph
from src.core.interfaces.my_json_serializable import MyJsonSerializable


class TSPProblem(MyJsonSerializable):
  """
  Travelling salesman problem (TSP) instance.
  """

  def __init__(self, name: str, graph: Graph) -> None:
    self.name = name
    self.graph = graph

  def to_json(self) -> dict:
    return {
      'instance_name': self.name,
      'distance_matrix': self.graph.to_json()['distance_matrix']
    }
