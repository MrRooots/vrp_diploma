from src.core.structures.graph import Graph


class IAlgorithm:
  """
  Algorithm base class
  """

  @staticmethod
  def run(graph: Graph, **kwargs) -> tuple[list, list] | tuple[list[int], float]:
    """ Start pure algorithm for given graph without binding to VRP task """
