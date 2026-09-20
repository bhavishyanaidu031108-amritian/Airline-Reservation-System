def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * n
    dist[source] = 0
    visited = set()

    while len(visited) < n:
        u = None
        minimum = float('inf')

        for v in range(n):
            if v not in visited and dist[v] < minimum:
                minimum = dist[v]
                u = v

        if u is None:
            break

        visited.add(u)

        for v in range(n):
            if graph[u][v] > 0 and v not in visited:
                new_dist = dist[u] + graph[u][v]

                if new_dist < dist[v]:
                    dist[v] = new_dist

    return dist


if __name__ == "__main__":
    graph = [
        [0, 4, 1, 0],
        [4, 0, 2, 1],
        [1, 2, 0, 5],
        [0, 1, 5, 0]
    ]

    source = 0

    result = dijkstra(graph, source)

    print("Shortest distances from source vertex", source)

    for i in range(len(result)):
        print("Vertex", i, ":", result[i])