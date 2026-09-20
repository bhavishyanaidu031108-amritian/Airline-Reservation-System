from DATABASE.db_connection import get_connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_number INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT,
            arrival_time TEXT,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL,
            fare REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY,
            passenger_id INTEGER NOT NULL,
            flight_number INTEGER NOT NULL,
            seat_number TEXT,
            booking_status TEXT NOT NULL,
            fare REAL NOT NULL,
            FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
            FOREIGN KEY (flight_number) REFERENCES flights(flight_number)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")