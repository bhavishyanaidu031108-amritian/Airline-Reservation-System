from DATABASE.db_connection import get_connection
from data_structures.priority_queue import WaitingList


class WaitingListService:
    def __init__(self):
        self.waiting_list = WaitingList()

    def add_to_waiting_list(self, passenger_id, priority):
        self.waiting_list.add_passenger(
            passenger_id,
            priority
        )

    def get_next_passenger(self):
        return self.waiting_list.get_next_passenger()

    def display_waiting_list(self):
        self.waiting_list.display()

    def get_queue_items(self):
        return sorted(self.waiting_list.queue)