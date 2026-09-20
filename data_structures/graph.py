class AirportGraph:
    def __init__(self):
        self.graph = {}

    def add_airport(self, airport):
        if airport not in self.graph:
            self.graph[airport] = []

    def add_route(self, source, destination, distance):
        self.add_airport(source)
        self.add_airport(destination)

        self.graph[source].append((destination, distance))

    def get_routes(self, airport):
        if airport in self.graph:
            return self.graph[airport]

        return []

    def display(self):
        for airport in self.graph:
            print(airport, "->", self.graph[airport])