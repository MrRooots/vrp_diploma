from typing import Type

from src.core.interfaces.i_vrp_solver import IVRPSolver
from src.core.structures.graph import Graph


class VRPSolver:
  """
  Class that solves vehicle routing problem with given graph
  """

  # Graph for the current problem
  __graph: Graph = None

  # The source node for the graph
  __source_node: int = None

  # The destination node for the VRP task
  __destination_node: int = None

  # The nodes that we have to pass through
  __target_nodes: list[int] = None

  def __init__(self,
               graph: Graph,
               source_node: int = None,
               destination_node: int = None,
               target_nodes: list[int] = None) -> None:
    self.__graph = graph
    self.__source_node = source_node
    self.__destination_node = destination_node
    self.__target_nodes = target_nodes

  @property
  def source(self) -> int:
    """ Get source node """
    return self.__source_node or 0

  @property
  def destination(self) -> int:
    """ Get destination node """
    return self.__destination_node or self.__graph.vertex_count - 1

  @property
  def targets(self) -> list[int]:
    """ Get target nodes """
    return self.__target_nodes or []

  def set_source_node(self, node: int) -> None:
    """ Set the given node as a source """
    self.__source_node = node

  def set_destination_node(self, node: int) -> None:
    """ Set the given node as a destination """
    self.__destination_node = node

  def set_target_nodes(self, nodes: list[int]) -> None:
    """ Set the given nodes as a target nodes """
    self.__target_nodes = nodes

  def __print_report(self, path: str, length: float):
    """ Print report for the solution """
    report = 'Shortest path from {} to {} is {} with weight {}'

    print(report.format(self.source, self.destination, path, length))

  def solve_vrp(self,
                solver: Type[IVRPSolver],
                report: bool = False) -> tuple[str, float]:
    """ Solve vehicle routing problem for current graph and params """
    path, length = solver.solve_vrp(self.__graph,
                                    self.source,
                                    self.destination,
                                    self.targets)

    if report:
      self.__print_report(path, length)

    return path, length
