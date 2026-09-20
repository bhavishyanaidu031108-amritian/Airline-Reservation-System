from DATABASE.db_connection import get_connection
from data_structures.avl_tree import AVLTree


class FlightService:
    def __init__(self):
        self.flight_tree = AVLTree()
        self.load_flights()

    def load_flights(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()

        connection.close()

        for flight in flights:
            self.flight_tree.root = self.flight_tree.insert(
                self.flight_tree.root,
                flight[0],
                flight
            )

    def add_flight(
        self,
        flight_number,
        source,
        destination,
        departure_time,
        arrival_time,
        total_seats,
        available_seats,
        fare
    ):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO flights
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            flight_number,
            source,
            destination,
            departure_time,
            arrival_time,
            total_seats,
            available_seats,
            fare
        ))

        connection.commit()
        connection.close()

        self.flight_tree.root = self.flight_tree.insert(
            self.flight_tree.root,
            flight_number,
            (
                flight_number,
                source,
                destination,
                departure_time,
                arrival_time,
                total_seats,
                available_seats,
                fare
            )
        )

    def search_flight(self, flight_number):
        node = self.flight_tree.search(
            self.flight_tree.root,
            flight_number
        )

        if node:
            return node.data

        return None

    def delete_flight(self, flight_number):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM flights WHERE flight_number = ?",
            (flight_number,)
        )

        connection.commit()
        connection.close()

        self.flight_tree.root = self.flight_tree.delete(
            self.flight_tree.root,
            flight_number
        )

    def display_flights(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()

        connection.close()

        for flight in flights:
            print(flight)

    def get_all_flights(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT flight_number, source, destination, departure_time, arrival_time, total_seats, available_seats, fare FROM flights ORDER BY flight_number")
        flights = cursor.fetchall()

        connection.close()
        return flights

    def update_flight(
        self,
        flight_number,
        source,
        destination,
        departure_time,
        arrival_time,
        total_seats,
        available_seats,
        fare
    ):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE flights
            SET source = ?, destination = ?, departure_time = ?, arrival_time = ?,
                total_seats = ?, available_seats = ?, fare = ?
            WHERE flight_number = ?
        """, (
            source,
            destination,
            departure_time,
            arrival_time,
            total_seats,
            available_seats,
            fare,
            flight_number
        ))

        connection.commit()
        connection.close()

        # Update AVL tree
        self.flight_tree.root = self.flight_tree.delete(
            self.flight_tree.root,
            flight_number
        )
        self.flight_tree.root = self.flight_tree.insert(
            self.flight_tree.root,
            flight_number,
            (
                flight_number,
                source,
                destination,
                departure_time,
                arrival_time,
                total_seats,
                available_seats,
                fare
            )
        )

    def search_flights_by_route(self, source=None, destination=None):
        connection = get_connection()
        cursor = connection.cursor()

        query = "SELECT flight_number, source, destination, departure_time, arrival_time, total_seats, available_seats, fare FROM flights WHERE 1=1"
        params = []

        if source and source != "All Sources" and source.strip():
            query += " AND LOWER(source) = LOWER(?)"
            params.append(source.strip())

        if destination and destination != "All Destinations" and destination.strip():
            query += " AND LOWER(destination) = LOWER(?)"
            params.append(destination.strip())

        cursor.execute(query, params)
        flights = cursor.fetchall()
        connection.close()
        return flights