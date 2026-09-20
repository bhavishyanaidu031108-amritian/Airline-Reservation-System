from DATABASE.db_connection import get_connection


class RevenueService:

    def calculate_total_revenue(self):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(fare), 0)
            FROM bookings
            WHERE booking_status = 'Confirmed'
        """)

        result = cursor.fetchone()[0]

        connection.close()

        return result

    def flight_revenue(self, flight_number):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(fare), 0)
            FROM bookings
            WHERE flight_number = ?
            AND booking_status = 'Confirmed'
        """, (flight_number,))

        result = cursor.fetchone()[0]

        connection.close()

        return result

    def display_revenue(self):
        total = self.calculate_total_revenue()

        print("Total Revenue:", total)

    def get_revenue_analytics(self):
        connection = get_connection()
        cursor = connection.cursor()

        # Total revenue from confirmed bookings
        cursor.execute("""
            SELECT COALESCE(SUM(fare), 0)
            FROM bookings
            WHERE booking_status = 'Confirmed'
        """)
        total_revenue = cursor.fetchone()[0] or 0.0

        # Confirmed count
        cursor.execute("""
            SELECT COUNT(*)
            FROM bookings
            WHERE booking_status = 'Confirmed'
        """)
        confirmed_count = cursor.fetchone()[0] or 0

        # Cancelled count
        cursor.execute("""
            SELECT COUNT(*)
            FROM bookings
            WHERE booking_status = 'Cancelled'
        """)
        cancelled_count = cursor.fetchone()[0] or 0

        # Flight-level revenues
        cursor.execute("""
            SELECT f.flight_number, f.source, f.destination,
                   COUNT(CASE WHEN b.booking_status = 'Confirmed' THEN 1 END) as confirmed_seats,
                   COALESCE(SUM(CASE WHEN b.booking_status = 'Confirmed' THEN b.fare ELSE 0 END), 0) as revenue
            FROM flights f
            LEFT JOIN bookings b ON f.flight_number = b.flight_number
            GROUP BY f.flight_number, f.source, f.destination
            ORDER BY revenue DESC, f.flight_number ASC
        """)
        flight_revenues = cursor.fetchall()

        connection.close()

        avg_fare = round(total_revenue / confirmed_count, 2) if confirmed_count > 0 else 0.0

        return {
            "total_revenue": total_revenue,
            "confirmed_count": confirmed_count,
            "cancelled_count": cancelled_count,
            "avg_fare": avg_fare,
            "flight_revenues": flight_revenues
        }

