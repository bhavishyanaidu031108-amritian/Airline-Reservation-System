from DATABASE.db_connection import get_connection
from data_structures.avl_tree import AVLTree


class PassengerService:
    def __init__(self):
        self.passenger_tree = AVLTree()
        self.load_passengers()

    def load_passengers(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM passengers")
        passengers = cursor.fetchall()

        connection.close()

        for passenger in passengers:
            self.passenger_tree.root = self.passenger_tree.insert(
                self.passenger_tree.root,
                passenger[0],
                passenger
            )

    def add_passenger(self, passenger_id, name, phone, email):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO passengers
            VALUES (?, ?, ?, ?)
        """, (
            passenger_id,
            name,
            phone,
            email
        ))

        connection.commit()
        connection.close()

        self.passenger_tree.root = self.passenger_tree.insert(
            self.passenger_tree.root,
            passenger_id,
            (
                passenger_id,
                name,
                phone,
                email
            )
        )

    def search_passenger(self, passenger_id):
        node = self.passenger_tree.search(
            self.passenger_tree.root,
            passenger_id
        )

        if node:
            return node.data

        return None

    def delete_passenger(self, passenger_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM passengers WHERE passenger_id = ?",
            (passenger_id,)
        )

        connection.commit()
        connection.close()

        self.passenger_tree.root = self.passenger_tree.delete(
            self.passenger_tree.root,
            passenger_id
        )

    def display_passengers(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM passengers")
        passengers = cursor.fetchall()

        connection.close()

        for passenger in passengers:
            print(passenger)

    def get_all_passengers(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT passenger_id, name, phone, email FROM passengers ORDER BY passenger_id")
        passengers = cursor.fetchall()

        connection.close()
        return passengers

    def update_passenger(self, passenger_id, name, phone, email):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE passengers
            SET name = ?, phone = ?, email = ?
            WHERE passenger_id = ?
        """, (name, phone, email, passenger_id))

        connection.commit()
        connection.close()

        self.passenger_tree.root = self.passenger_tree.delete(
            self.passenger_tree.root,
            passenger_id
        )
        self.passenger_tree.root = self.passenger_tree.insert(
            self.passenger_tree.root,
            passenger_id,
            (passenger_id, name, phone, email)
        )