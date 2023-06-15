import json

from src.core.models.euclidean_norm import EuclideanNorm
from src.core.interfaces.my_json_serializable import MyJsonSerializable


class Depot(MyJsonSerializable, EuclideanNorm):
  def __init__(self, _id, x, y, demand, ready_time, due_time, service) -> None:
    self.id = 0
    self.x, self.y = x, y
    self.demand = demand
    self.ready_time = ready_time
    self.due_time = due_time
    self.service_time = service

  def to_json(self) -> dict:
    return {
      'coordinates': {
        'x': self.x,
        'y': self.y,
      },
      'demand': self.demand,
      'ready_time': self.ready_time,
      'due_time': self.due_time,
      'service_time': self.service_time,
    }

  def __str__(self) -> str:
    return json.dumps(self.to_json(), indent=2)
