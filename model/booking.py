from DATABASE.db_connection import get_connection
from data_structures.avl_tree import AVLTree


class BookingService:
    def __init__(self):
        self.booking_tree = AVLTree()
        self.load_bookings()

    def load_bookings(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()

        connection.close()

        for booking in bookings:
            self.booking_tree.root = self.booking_tree.insert(
                self.booking_tree.root,
                booking[0],
                booking
            )

    def create_booking(
        self,
        booking_id,
        passenger_id,
        flight_number,
        seat_number,
        booking_status,
        fare
    ):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bookings
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            booking_id,
            passenger_id,
            flight_number,
            seat_number,
            booking_status,
            fare
        ))

        cursor.execute("""
            UPDATE flights
            SET available_seats = available_seats - 1
            WHERE flight_number = ?
        """, (flight_number,))

        connection.commit()
        connection.close()

        self.booking_tree.root = self.booking_tree.insert(
            self.booking_tree.root,
            booking_id,
            (
                booking_id,
                passenger_id,
                flight_number,
                seat_number,
                booking_status,
                fare
            )
        )

    def search_booking(self, booking_id):
        node = self.booking_tree.search(
            self.booking_tree.root,
            booking_id
        )

        if node:
            return node.data

        return None

    def cancel_booking(self, booking_id):
        booking = self.search_booking(booking_id)

        if booking is None:
            return False

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE bookings SET booking_status = ? WHERE booking_id = ?",
            ("Cancelled", booking_id)
        )

        cursor.execute("""
            UPDATE flights
            SET available_seats = available_seats + 1
            WHERE flight_number = ?
        """, (booking[2],))

        connection.commit()
        connection.close()

        self.booking_tree.root = self.booking_tree.delete(
            self.booking_tree.root,
            booking_id
        )

        return True

    def display_bookings(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()

        connection.close()

        for booking in bookings:
            print(booking)