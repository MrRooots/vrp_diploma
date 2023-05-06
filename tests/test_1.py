import numpy as np


def johnson(graph):
  n = len(graph)
  new_graph = np.zeros((n + 1, n + 1))
  for i in range(n):
    new_graph[i][:n] = graph[i][:]
  new_graph[n][:n] = [float("inf")] * n
  new_graph[:n, n] = [0] * n
  dist = bellman_ford(new_graph, n)
  if dist == "negative cycle":
    return "Graph contains negative cycle"
  else:
    for i in range(n):
      for j in range(n):
        if graph[i][j] != 0:
          graph[i][j] += dist[i] - dist[j] + n
    res = np.zeros((n, n))
    for i in range(n):
      temp = dijkstra(graph, i)
      for j in range(n):
        res[i][j] = temp[j] - dist[i] + dist[j]
    return res


def bellman_ford(graph, s):
  dist = [float("inf")] * (len(graph))
  dist[s] = 0
  for i in range(len(graph) - 1):
    for u in range(len(graph)):
      for v in range(len(graph)):
        if graph[u][v] != 0:
          if dist[u] + graph[u][v] < dist[v]:
            dist[v] = dist[u] + graph[u][v]
  for u in range(len(graph)):
    for v in range(len(graph)):
      if graph[u][v] != 0:
        if dist[u] + graph[u][v] < dist[v]:
          return "negative cycle"
  return dist


def dijkstra(graph, s):
  n = len(graph)
  dist = [float("inf")] * n
  visited = [False] * n
  dist[s] = 0
  for _ in range(n):
    u = get_min_vertex(dist, visited)
    visited[u] = True
    for v in range(n):
      if graph[u][v] != 0 and not visited[v]:
        if dist[u] + graph[u][v] < dist[v]:
          dist[v] = dist[u] + graph[u][v]
  return dist


def get_min_vertex(dist, visited):
  min_dist = float("inf")
  min_vertex = -1
  for vertex in range(len(dist)):
    if not visited[vertex] and dist[vertex] < min_dist:
      min_dist = dist[vertex]
      min_vertex = vertex
  return min_vertex


if __name__ == '__main__':
  graph = [[0, 4, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, -2, 0, 5, 0],
           [0, 0, 0, 0, 1],
           [0, 0, 0, -2, 0]
           ]

  print(johnson(graph))
