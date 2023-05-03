from lib.src.structures.graph import Graph


class IVRPSolver:
  """
  Vehicle routing problem algorithms class.
  """

  @staticmethod
  def solve_vrp(graph: Graph,
                source: int,
                destination: int,
                targets: list[int]):
    """ Solve VRP problem for given graph """
