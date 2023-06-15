from __future__ import annotations

import json

from src.core.models.euclidean_norm import EuclideanNorm
from src.core.interfaces.my_json_serializable import MyJsonSerializable


class Customer(MyJsonSerializable, EuclideanNorm):
  """
  Customer instance
  """

  def __init__(self, _id, x, y, demand, ready_time, due_date, service) -> None:
    self.id = int(_id)
    self.x, self.y = x, y
    self.demand = demand
    self.ready_time = ready_time
    self.due_time = due_date
    self.service_time = service
    self.is_serviced = False

  def to_json(self) -> dict:
    return {
      f'customer_{self.id}': {
        'id': self.id,
        'coordinates': {
          'x': self.x,
          'y': self.y,
        },
        'demand': self.demand,
        'ready_time': self.ready_time,
        'due_time': self.due_time,
        'service_time': self.service_time,
      }
    }

  def __str__(self):
    return json.dumps(self.to_json(), indent=2)
