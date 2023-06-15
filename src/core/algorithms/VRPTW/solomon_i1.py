from src.core.models.problem import Problem
from src.core.utils.decorators import Decorators
from src.core.utils.utilities import Utilities


class SolomonI1:
  """
  Solomon Insertion Heuristic.

  Main idea in iteratively inserting customers into existing routes
  based on the minimum cost increase criterion.
  By inserting customers strategically, the algorithm aims to minimize
  the total distance or cost of the routes.

  The improvement phase helps refine the solution further by searching
  for local optima.
  It's important to note that the Solomon I1 heuristic is a simple
  and efficient approach but may not always produce the optimal solution
  for complex instances of the VRP.

  However, it can serve as a good initial solution or as a baseline
  for more sophisticated algorithms.
  """

  @staticmethod
  @Decorators.convert_to_result_model
  def run(unrouted_customers: list[int], problem: Problem):
    """
    Execute Solomon I1 Insertion Method.

    References
      [1]: Marius M. Solomon, (1987) Algorithms for the Vehicle Routing and
      Scheduling Problems with Time Window Constraints. Operations Research
      Points: 1.3, 3.1
    """
    # mu, lamda, a1, a2 = 1, 2, 0, 1  # [Original]
    mu, lamda, a1, a2 = 1, 2, 1, 0
    solution = []

    while len(unrouted_customers) != 0:
      # Route init: [ 0, FURTHEST, 0 ] and remove FURTHEST from unrouted
      unrouted_cust_distance = [problem.matrix[0][i] for i in unrouted_customers]
      furthest_index = unrouted_cust_distance.index(max(unrouted_cust_distance))

      tour = [0, unrouted_customers[furthest_index], 0]
      del unrouted_customers[furthest_index]

      # Heuristic Insertion-Criterion 1
      while True:
        # Calculate c1
        insert_position, feasible_cust, c1 = [], [], []

        for i in range(len(unrouted_customers)):
          u = unrouted_customers[i]
          min_cost = float("inf")
          position = -1

          for p in range(len(tour) - 1):
            # Insert new order [u] on position [p] and recalculate constraints
            new_tour = tour[:p + 1] + [u] + tour[p + 1:]
            time_check_passed = Utilities.time_checker(new_tour, problem)
            new_capacity = sum(c.demand for c in problem.get_customers_by_id(new_tour))

            # Check time and capacity constraints
            if time_check_passed and new_capacity <= problem.vehicle_capacity:
              # Calculate parameters c11 and c12 according to [1. point 1.3 i)]
              # This type of insertion heuristics tries to maximize the benefit
              # derived from servicing a customer on the partial route
              # being constructed rather than on a direct route
              # c11(p - 1, u, p + 1) = d(p - 1, u) + d(u, p + 1) - mu * d(p - 1, p + 1),
              # c11(p - 1, u, p + 1) = b(u, p + 2) - b(p + 1),
              # cost = a1 * c11 + a2 * c12
              # Where d - distance,
              #       b - new time for service to begin, considering u is on the route
              #       a1 + a2 = 1
              c11: float = (problem.matrix[tour[p]][u]
                            + problem.matrix[u][tour[p + 1]]
                            - mu * problem.matrix[tour[p]][tour[p + 1]])
              c12: float = (
                      Utilities.begin_time(new_tour, problem)[p + 2] -
                      Utilities.begin_time(tour, problem)[p + 1]
              )
              cost = a1 * c11 + a2 * c12

              # Update optimal cost and position
              if cost < min_cost:
                min_cost = cost
                position = p

          # If optimal cost found then add u to feasible customers
          if position != -1:
            feasible_cust.append(u)
            insert_position.append(position)
            c1.append(min_cost)

        # Calculate parameter c2 according to [1. point 1.3 i)]
        # c2(p - 1, u, p + 1) = lamda * d(0, u) - c1(p - 1, u, p + 1)
        # Where lamda >= 0
        if feasible_cust:
          c2 = []
          for i in range(len(feasible_cust)):
            cost2 = lamda * problem.matrix[0][feasible_cust[i]] - c1[i]
            c2.append(cost2)

          optimal_ind = c2.index(max(c2))

          # Insert optimal customer to the tour
          tour.insert(insert_position[optimal_ind] + 1,
                      feasible_cust[optimal_ind])

          unrouted_customers.remove(feasible_cust[optimal_ind])

        else:
          break

      solution.append(tour)

    return solution, [sum(i) for i in solution]
