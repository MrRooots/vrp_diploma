def dijkstra(graph, start, destination=None):
  n = len(graph)
  distances = [float('inf')] * n
  predecessor = [-1] * n
  visited = [False] * n
  distances[start] = 0

  while not visited[destination] if destination else all(visited):
    # Find the unvisited node with the smallest distance
    min_vertex = min(
      (u for u in range(n) if not visited[u]), key=lambda x: distances[x]
    )
    
    visited[min_vertex] = True

    # Update the distances of the neighbors
    for v in range(n):
      if graph[min_vertex][v] > 0 and not visited[v]:
        new_distance = distances[min_vertex] + graph[min_vertex][v]
        if new_distance < distances[v]:
          distances[v] = new_distance
          predecessor[v] = min_vertex

  return distances, predecessor


def shortest_path(graph, source, destination):
  distances, predecessor = dijkstra(graph, source, destination)
  path = []
  vertex = destination

  while vertex != -1:
    path.append(vertex)
    vertex = predecessor[vertex]

  return f'Shortest path from {source} to {destination} is {list(reversed(path))} with weight {distances[destination]}'


source = 0
# destination = 5


adj_matrix = [
  [0, 4, 0, 0, 0, 0, 0, 8, 0],
  [4, 0, 8, 0, 0, 0, 0, 11, 0],
  [0, 8, 0, 7, 0, 4, 0, 0, 2],
  [0, 0, 7, 0, 9, 14, 0, 0, 0],
  [0, 0, 0, 9, 0, 10, 0, 0, 0],
  [0, 0, 4, 14, 10, 0, 2, 0, 0],
  [0, 0, 0, 0, 0, 2, 0, 1, 6],
  [8, 11, 0, 0, 0, 0, 1, 0, 7],
  [0, 0, 2, 0, 0, 0, 6, 7, 0]
]

# adj_matrix = [
#   [0, 2, 4, 0, 0, 0],
#   [2, 0, 3, 8, 0, 0],
#   [4, 3, 0, 2, 5, 0],
#   [0, 8, 2, 0, 11, 22],
#   [0, 0, 5, 11, 0, 1],
#   [0, 0, 0, 22, 1, 0],
# ]

# GraphVisualization(GraphGenerator.from_adjacency_matrix(adj_matrix)).visualize(add_weight_labels=True)


for destination in range(len(adj_matrix)):
  print(shortest_path(adj_matrix, source, destination))
