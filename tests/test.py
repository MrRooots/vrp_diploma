import networkx


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


from collections import defaultdict

MAX_INT = float('Inf')


def minDistance(dist, visited):
  (minimum, minVertex) = (MAX_INT, 0)
  for vertex in range(len(dist)):
    if minimum > dist[vertex] and visited[vertex] == False:
      (minimum, minVertex) = (dist[vertex], vertex)

  return minVertex


def Dijkstra(graph, modifiedGraph, src):
  num_vertices = len(graph)

  sptSet = defaultdict(lambda: False)
  dist = [MAX_INT] * num_vertices
  dist[src] = 0

  for count in range(num_vertices):

    curVertex = minDistance(dist, sptSet)
    sptSet[curVertex] = True

    for vertex in range(num_vertices):
      if ((sptSet[vertex] == False) and
              (dist[vertex] > (dist[curVertex] +
                               modifiedGraph[curVertex][vertex])) and
              (graph[curVertex][vertex] != 0)):
        dist[vertex] = (dist[curVertex] +
                        modifiedGraph[curVertex][vertex]);

  for vertex in range(num_vertices):
    print('Vertex ' + str(vertex) + ': ' + str(dist[vertex]))


def BellmanFord(edges, graph, num_vertices):
  dist = [MAX_INT] * (num_vertices + 1)
  dist[num_vertices] = 0

  for i in range(num_vertices):
    edges.append([num_vertices, i, 0])

  for i in range(num_vertices):
    for (src, des, weight) in edges:
      if ((dist[src] != MAX_INT) and
              (dist[src] + weight < dist[des])):
        dist[des] = dist[src] + weight

  return dist[0:num_vertices]


def JohnsonAlgorithm(graph):
  edges = []

  for i in range(len(graph)):
    for j in range(len(graph[i])):

      if graph[i][j] != 0:
        edges.append([i, j, graph[i][j]])

  modifyWeights = BellmanFord(edges, graph, len(graph))

  modifiedGraph = [[0 for x in range(len(graph))] for y in
                   range(len(graph))]

  for i in range(len(graph)):
    for j in range(len(graph[i])):

      if graph[i][j] != 0:
        modifiedGraph[i][j] = (graph[i][j] +
                               modifyWeights[i] - modifyWeights[j]);

  print('Modified Graph: ' + str(modifiedGraph))

  for src in range(len(graph)):
    print('\nShortest Distance with vertex ' +
          str(src) + ' as the source:\n')
    Dijkstra(graph, modifiedGraph, src)


graph = [[0, -8, 2, 4],
         [0, 0, 2, 6],
         [0, 0, 0, 2],
         [0, 0, 0, 0]]

JohnsonAlgorithm(graph)

# Driver Code
graph = [[0, -5, 2, 3],
         [0, 0, 4, 0],
         [0, 0, 0, 1],
         [0, 0, 0, 0]]
#
# johnson(graph)
networkx.johnson()
# source = 0
# # destination = 5
#
#
# adj_matrix = [
#   [0, 4, 0, 0, 0, 0, 0, 8, 0],
#   [4, 0, 8, 0, 0, 0, 0, 11, 0],
#   [0, 8, 0, 7, 0, 4, 0, 0, 2],
#   [0, 0, 7, 0, 9, 14, 0, 0, 0],
#   [0, 0, 0, 9, 0, 10, 0, 0, 0],
#   [0, 0, 4, 14, 10, 0, 2, 0, 0],
#   [0, 0, 0, 0, 0, 2, 0, 1, 6],
#   [8, 11, 0, 0, 0, 0, 1, 0, 7],
#   [0, 0, 2, 0, 0, 0, 6, 7, 0]
# ]

# adj_matrix = [
#   [0, 2, 4, 0, 0, 0],
#   [2, 0, 3, 8, 0, 0],
#   [4, 3, 0, 2, 5, 0],
#   [0, 8, 2, 0, 11, 22],
#   [0, 0, 5, 11, 0, 1],
#   [0, 0, 0, 22, 1, 0],
# ]

# GraphVisualization(GraphGenerator.from_adjacency_matrix(adj_matrix)).visualize(add_weight_labels=True)


# for destination in range(len(adj_matrix)):
#   print(shortest_path(adj_matrix, source, destination))
