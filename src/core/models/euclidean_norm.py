from __future__ import annotations


class EuclideanNorm:
  x: float
  y: float

  def calculate_distance_to(self, p2) -> float:
    """
    Calculate distance between two points

    Both points - objects with `x: float` and `y: float` attributes
    """
    return ((self.x - p2.x) ** 2 + (self.y - p2.y) ** 2) ** 0.5
