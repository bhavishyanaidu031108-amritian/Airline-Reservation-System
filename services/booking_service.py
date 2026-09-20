from DATABASE.db_connection import get_connection
try:
    from data_structures.avl_tree import AVLTree
except ModuleNotFoundError:
    from data_structures.AVL_tree import AVLTree


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

    def get_all_bookings(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT b.booking_id, b.passenger_id, p.name, b.flight_number,
                   f.source, f.destination, b.seat_number, b.booking_status, b.fare
            FROM bookings b
            LEFT JOIN passengers p ON b.passenger_id = p.passenger_id
            LEFT JOIN flights f ON b.flight_number = f.flight_number
            ORDER BY b.booking_id DESC
        """)
        bookings = cursor.fetchall()

        connection.close()
        return bookings

    def get_passenger_bookings(self, passenger_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT b.booking_id, b.passenger_id, p.name, b.flight_number,
                   f.source, f.destination, b.seat_number, b.booking_status, b.fare
            FROM bookings b
            LEFT JOIN passengers p ON b.passenger_id = p.passenger_id
            LEFT JOIN flights f ON b.flight_number = f.flight_number
            WHERE b.passenger_id = ?
            ORDER BY b.booking_id DESC
        """, (passenger_id,))
        bookings = cursor.fetchall()

        connection.close()
        return bookings

    def get_booked_seats_for_flight(self, flight_number):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT seat_number
            FROM bookings
            WHERE flight_number = ? AND booking_status = 'Confirmed'
        """, (flight_number,))
        seats = [row[0] for row in cursor.fetchall() if row[0]]

        connection.close()
        return seats