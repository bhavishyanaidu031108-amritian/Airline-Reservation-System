import heapq


class WaitingList:
    def __init__(self):
        self.queue = []

    def add_passenger(self, passenger_id, priority):
        heapq.heappush(
            self.queue,
            (priority, passenger_id)
        )

    def get_next_passenger(self):
        if self.queue:
            return heapq.heappop(self.queue)

        return None

    def display(self):
        print("Waiting List:")

        for priority, passenger_id in sorted(self.queue):
            print(
                "Passenger ID:",
                passenger_id,
                "Priority:",
                priority
            )