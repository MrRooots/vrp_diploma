import json

from src.core.models.customer import Customer
from src.core.models.depot import Depot
from src.core.models.graph import Graph
from src.core.interfaces.my_json_serializable import MyJsonSerializable


class Problem(MyJsonSerializable):
  """
  Vehicle routing problem (VRP) instance.
  """
  name: str
  max_vehicle: int
  vehicle_capacity: float
  depot: Depot
  customers: list[Customer]
  graph: Graph

  def __init__(self,
               name: str,
               max_vehicle: int,
               vehicle_capacity: float,
               depot: Depot,
               customers: list[Customer],
               graph: Graph) -> None:
    self.name = name
    self.max_vehicle = max_vehicle
    self.vehicle_capacity = vehicle_capacity
    self.customers: list[Customer] = customers
    self.depot = depot
    self.graph = graph

  def __str__(self) -> str:
    return json.dumps(self.to_json(), indent=2)

  @property
  def matrix(self) -> list[list[float]]:
    return self.graph.matrix

  @property
  def nodes(self) -> list[Customer | Depot]:
    return [self.depot, *self.customers]

  @property
  def get_coords(self) -> tuple[list[float], list[float]]:
    return [c.x for c in self.nodes], [c.y for c in self.nodes]

  @property
  def customers_count(self) -> int:
    return len(self.customers)

  def get_customer_by_id(self, _id: int) -> Customer:
    """ Get customer by its identifier """
    return self.nodes[_id]

  def get_customers_by_id(self, ids: list[int]) -> list[Customer]:
    """ Get customers by given list of identifiers """
    return [self.get_customer_by_id(_id) for _id in ids]

  def get_total_demand_for(self, ids: list[int]) -> float:
    """ Get total demand for requested customers """
    return sum(i.demand for i in self.get_customers_by_id(ids))

  def to_json(self) -> dict:
    return {
      'instance_name': self.name,
      'max_vehicle_number': self.max_vehicle,
      'vehicle_capacity': self.vehicle_capacity,
      'depart': self.depot.to_json(),
      'customers': [
        c.to_json() for c in self.customers
      ],
      'distance_matrix': self.graph.to_json()['distance_matrix']
    }
