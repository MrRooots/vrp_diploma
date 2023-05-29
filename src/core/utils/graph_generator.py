import ast
import json
import os
from src.core.structures.graph import Graph


class GraphGenerator:
  """
  GraphGenerator class.
  """

  @staticmethod
  def from_adjacency_matrix(matrix: list[list[float]]) -> Graph:
    """ Generate `Graph` from given `matrix` """
    return Graph(matrix)

  @staticmethod
  def from_file(filename: str) -> Graph:
    """ Generate `Graph` from given file """
    with open(f'data/input/{filename}', 'r') as file:
      matrix = [
        [float(v) if v != '0' else None for v in line.split()]
        for line in file
      ]
      layout = None
      if os.path.isfile(f'data/input/layouts/layout_{filename}'):
        with open(f'data/input/layouts/layout_{filename}', 'r') as f:
          layout = ast.literal_eval(f.readline())

    return Graph(matrix, layout)
