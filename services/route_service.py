from data_structures.graph import AirportGraph
from algorithms.dijkstra import dijkstra


class RouteService:
    def __init__(self):
        self.graph = AirportGraph()
        self.airports = []
        self.create_network()

    def create_network(self):
        routes = [
            ("Hyderabad", "Chennai", 630),
            ("Hyderabad", "Bangalore", 570),
            ("Bangalore", "Mumbai", 980),
            ("Chennai", "Mumbai", 1330)
        ]

        for source, destination, distance in routes:
            self.graph.add_route(
                source,
                destination,
                distance
            )

        self.airports = list(self.graph.graph.keys())

    def shortest_route(self, source):
        if source not in self.airports:
            return None

        source_index = self.airports.index(source)

        n = len(self.airports)

        matrix = [
            [0 for _ in range(n)]
            for _ in range(n)
        ]

        for airport in self.graph.graph:
            i = self.airports.index(airport)

            for destination, distance in self.graph.graph[airport]:
                j = self.airports.index(destination)
                matrix[i][j] = distance

        distances = dijkstra(
            matrix,
            source_index
        )

        result = {}

        for i in range(n):
            result[self.airports[i]] = distances[i]

        return result

    def get_airports(self):
        return list(self.airports)

    def get_all_routes(self):
        routes = []
        for src in self.graph.graph:
            for dst, dist in self.graph.graph[src]:
                routes.append((src, dst, dist))
        return routes

    def find_shortest_path(self, source, destination):
        if source not in self.airports or destination not in self.airports:
            return None, float('inf')

        if source == destination:
            return [source], 0

        source_index = self.airports.index(source)
        dest_index = self.airports.index(destination)
        n = len(self.airports)

        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for airport in self.graph.graph:
            i = self.airports.index(airport)
            for dest, dist in self.graph.graph[airport]:
                j = self.airports.index(dest)
                matrix[i][j] = dist

        distances = dijkstra(matrix, source_index)

        if distances[dest_index] == float('inf'):
            return None, float('inf')

        path = [self.airports[dest_index]]
        curr = dest_index
        visited = set([curr])

        while curr != source_index:
            found = False
            for p in range(n):
                if matrix[p][curr] > 0 and distances[curr] == distances[p] + matrix[p][curr]:
                    curr = p
                    path.append(self.airports[curr])
                    visited.add(p)
                    found = True
                    break
            if not found:
                break

        path.reverse()
        return path, distances[dest_index]