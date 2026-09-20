"""
Automated Verification Test Suite for SkyLink Airline Reservation System.
Tests all backend data structures, services, algorithms, and GUI view instantiation.
"""

import sys
import os
import unittest

# Ensure workspace root is in path
workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

from DATABASE.schema import create_tables
from services.flight_service import FlightService
from services.passenger_service import PassengerService
from services.booking_service import BookingService
from services.waiting_list_service import WaitingListService
from services.route_service import RouteService
from services.revenue_service import RevenueService
from services.auth_service import AuthService
from algorithms.dijkstra import dijkstra


class TestSkyLinkBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_tables()

    def test_flight_service_and_avl(self):
        fs = FlightService()
        flights = fs.get_all_flights()
        self.assertGreater(len(flights), 0, "Flights table should not be empty")

        # Test AVL tree search
        f101 = fs.search_flight(101)
        self.assertIsNotNone(f101, "Flight 101 should exist in AVL tree")
        self.assertEqual(f101[0], 101)
        self.assertEqual(f101[1], "Hyderabad")

    def test_passenger_service_and_avl(self):
        ps = PassengerService()
        passengers = ps.get_all_passengers()
        self.assertGreater(len(passengers), 0, "Passengers table should not be empty")

        # Test AVL search
        p1001 = ps.search_passenger(1001)
        self.assertIsNotNone(p1001, "Passenger 1001 should exist in AVL tree")
        self.assertEqual(p1001[0], 1001)

    def test_booking_service(self):
        bs = BookingService()
        bookings = bs.get_all_bookings()
        self.assertGreater(len(bookings), 0, "Bookings should exist")

    def test_dijkstra_shortest_route(self):
        rs = RouteService()
        path, dist = rs.find_shortest_path("Hyderabad", "Mumbai")
        self.assertEqual(path, ["Hyderabad", "Bangalore", "Mumbai"])
        self.assertEqual(dist, 1550)

    def test_waiting_list_priority_queue(self):
        wls = WaitingListService()
        wls.add_to_waiting_list("P9999", 1)
        items = wls.get_queue_items()
        self.assertTrue(any(item[1] == "P9999" for item in items))

    def test_revenue_service(self):
        revs = RevenueService()
        analytics = revs.get_revenue_analytics()
        self.assertIn("total_revenue", analytics)
        self.assertIn("confirmed_count", analytics)
        self.assertIn("flight_revenues", analytics)
        self.assertGreaterEqual(analytics["total_revenue"], 0)

    def test_auth_service(self):
        auth = AuthService()
        self.assertEqual(auth.authenticate("admin", "admin123"), "Admin")
        self.assertEqual(auth.authenticate("bhavishya", "pass123"), "Passenger")
        self.assertIsNone(auth.authenticate("admin", "wrongpassword"))


class TestSkyLinkGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import customtkinter as ctk
        cls.ctk = ctk
        cls.root = ctk.CTk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_views_instantiation(self):
        from GUI.dashboard import DashboardView
        from GUI.flight_view import FlightView
        from GUI.flight_search_window import FlightSearchView
        from GUI.passenger_view import PassengerView
        from GUI.booking_view import BookingView
        from GUI.cancellation_view import CancellationView
        from GUI.waiting_list_view import WaitingListView
        from GUI.route_view import RouteView
        from GUI.revenue_view import RevenueView
        from GUI.settings_view import SettingsView
        from GUI.login_window import LoginWindow
        from GUI.main_window import MainWindow

        # Test view creations inside root
        parent = self.ctk.CTkFrame(self.root)
        parent.pack()

        v_dash = DashboardView(parent)
        self.assertIsNotNone(v_dash)

        v_flight = FlightView(parent)
        self.assertIsNotNone(v_flight)

        v_search = FlightSearchView(parent)
        self.assertIsNotNone(v_search)

        v_pass = PassengerView(parent)
        self.assertIsNotNone(v_pass)

        v_book = BookingView(parent)
        self.assertIsNotNone(v_book)

        v_cancel = CancellationView(parent)
        self.assertIsNotNone(v_cancel)

        v_wait = WaitingListView(parent)
        self.assertIsNotNone(v_wait)

        v_route = RouteView(parent)
        self.assertIsNotNone(v_route)

        v_rev = RevenueView(parent)
        self.assertIsNotNone(v_rev)

        v_sett = SettingsView(parent)
        self.assertIsNotNone(v_sett)

        v_login = LoginWindow(parent)
        self.assertIsNotNone(v_login)

        v_main = MainWindow(parent, user_info={"username": "admin", "role": "Admin"})
        self.assertIsNotNone(v_main)

        parent.destroy()


if __name__ == "__main__":
    unittest.main()
