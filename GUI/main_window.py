"""
Main Window Orchestrator for SkyLink Airline Reservation System.
Coordinates the modern collapsible sidebar, live header, and dynamic view routing
between all system modules (Dashboard, Flights, Bookings, Routes, Revenue, etc.).
"""

import customtkinter as ctk
from GUI.components.sidebar import Sidebar
from GUI.components.header import Header
from GUI.components.theme import COLOR_BG_LIGHT

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


class MainWindow(ctk.CTkFrame):
    def __init__(self, master, user_info=None, on_logout=None, **kwargs):
        super().__init__(master, fg_color=COLOR_BG_LIGHT, corner_radius=0, **kwargs)
        self.master = master
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.on_logout = on_logout

        self.active_view_key = "dashboard"
        self.view_instances = {}

        self._build_layout()
        self.navigate_to("dashboard")

    def _build_layout(self):
        # 1. Left Navigation Sidebar
        self.sidebar = Sidebar(
            self,
            current_view="dashboard",
            on_navigate=self.navigate_to,
            role=self.user_info.get("role", "Admin"),
            on_logout=self.on_logout
        )
        self.sidebar.pack(side="left", fill="y")

        # 2. Right Content Wrapper
        self.right_wrapper = ctk.CTkFrame(self, fg_color=COLOR_BG_LIGHT, corner_radius=0)
        self.right_wrapper.pack(side="right", fill="both", expand=True)

        # 3. Top Header
        self.header = Header(
            self.right_wrapper,
            username=self.user_info.get("username", "Admin"),
            role=self.user_info.get("role", "Admin"),
            on_logout=self.on_logout
        )
        self.header.pack(fill="x", padx=16, pady=(16, 12))

        # 4. View Container Frame
        self.view_container = ctk.CTkFrame(self.right_wrapper, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def navigate_to(self, view_key, extra_args=None):
        """
        Switches the currently displayed content view.
        """
        self.active_view_key = view_key
        self.sidebar.set_active_view(view_key)

        # Clear existing view children
        for child in self.view_container.winfo_children():
            child.destroy()

        # Instantiate target view
        new_view = self._create_view(view_key, extra_args)
        if new_view:
            new_view.pack(fill="both", expand=True)

    def _create_view(self, key, extra_args=None):
        extra_args = extra_args or {}

        if key == "dashboard":
            return DashboardView(
                self.view_container,
                user_info=self.user_info,
                on_navigate=self.navigate_to
            )
        elif key == "flights":
            return FlightView(
                self.view_container,
                user_info=self.user_info,
                on_book_flight=lambda f_data: self.navigate_to("bookings", {"preselected_flight": f_data})
            )
        elif key == "search":
            return FlightSearchView(
                self.view_container,
                on_book_flight=lambda f_data: self.navigate_to("bookings", {"preselected_flight": f_data})
            )
        elif key == "passengers":
            return PassengerView(
                self.view_container,
                user_info=self.user_info
            )
        elif key == "bookings":
            return BookingView(
                self.view_container,
                preselected_flight=extra_args.get("preselected_flight"),
                user_info=self.user_info
            )
        elif key == "cancellation":
            return CancellationView(
                self.view_container,
                user_info=self.user_info
            )
        elif key == "waiting_list":
            return WaitingListView(
                self.view_container,
                user_info=self.user_info
            )
        elif key == "routes":
            return RouteView(
                self.view_container,
                user_info=self.user_info
            )
        elif key == "revenue":
            return RevenueView(
                self.view_container,
                user_info=self.user_info
            )
        elif key == "settings":
            return SettingsView(
                self.view_container,
                user_info=self.user_info
            )
        else:
            return DashboardView(self.view_container, user_info=self.user_info, on_navigate=self.navigate_to)
