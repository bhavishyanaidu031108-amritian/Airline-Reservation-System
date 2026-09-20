"""
Main Airline Dashboard view for SkyLink.
Displays 4 elevated KPI statistics cards, simulated live flight departure status board,
and quick operation shortcuts.
"""

import customtkinter as ctk
from services.flight_service import FlightService
from services.passenger_service import PassengerService
from services.booking_service import BookingService
from services.revenue_service import RevenueService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_ACCENT_SKY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, FONT_TITLE,
    FONT_SECTION, FONT_BODY, FONT_SMALL
)
from GUI.components.cards import StatCard
from GUI.components.tables import ModernTable


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, user_info=None, on_navigate=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.on_navigate = on_navigate

        self.flight_service = FlightService()
        self.passenger_service = PassengerService()
        self.booking_service = BookingService()
        self.revenue_service = RevenueService()

        self._build_ui()

    def _build_ui(self):
        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=4, pady=4)

        # ----------------------------------------------------
        # 1. KPI STATISTIC CARDS (4 Column Grid)
        # ----------------------------------------------------
        cards_grid = ctk.CTkFrame(scrollable, fg_color="transparent")
        cards_grid.pack(fill="x", pady=(0, 20))

        # Fetch real metrics from services
        flights = self.flight_service.get_all_flights()
        passengers = self.passenger_service.get_all_passengers()
        all_bookings = self.booking_service.get_all_bookings()
        active_bookings_count = sum(1 for b in all_bookings if b[7] == "Confirmed")
        total_revenue = self.revenue_service.calculate_total_revenue()

        # Grid configuration for 4 cards
        cards_grid.columnconfigure((0, 1, 2, 3), weight=1, uniform="stat_cards")

        self.card_flights = StatCard(
            cards_grid,
            title="Total Flights",
            target_value=len(flights),
            icon="🛫",
            subtitle=f"{len(flights)} Scheduled Routes"
        )
        self.card_flights.grid(row=0, column=0, padx=6, pady=4, sticky="nsew")

        self.card_passengers = StatCard(
            cards_grid,
            title="Total Passengers",
            target_value=len(passengers),
            icon="👤",
            subtitle=f"{len(passengers)} Registered Travellers"
        )
        self.card_passengers.grid(row=0, column=1, padx=6, pady=4, sticky="nsew")

        self.card_bookings = StatCard(
            cards_grid,
            title="Active Bookings",
            target_value=active_bookings_count,
            icon="🎫",
            subtitle=f"{active_bookings_count} Confirmed Tickets"
        )
        self.card_bookings.grid(row=0, column=2, padx=6, pady=4, sticky="nsew")

        self.card_revenue = StatCard(
            cards_grid,
            title="Total Revenue",
            target_value=total_revenue,
            icon="₹",
            is_currency=True,
            subtitle="Calculated from Bookings"
        )
        self.card_revenue.grid(row=0, column=3, padx=6, pady=4, sticky="nsew")

        # ----------------------------------------------------
        # 2. QUICK ACTIONS BAR
        # ----------------------------------------------------
        actions_bar = ctk.CTkFrame(
            scrollable,
            fg_color=COLOR_BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER,
            height=64
        )
        actions_bar.pack(fill="x", pady=(0, 20))
        actions_bar.pack_propagate(False)

        lbl_quick = ctk.CTkLabel(
            actions_bar,
            text="⚡ Quick Actions:",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_quick.pack(side="left", padx=20)

        # Action buttons
        btn_book = ctk.CTkButton(
            actions_bar,
            text="+ Book Flight Ticket",
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            corner_radius=8,
            font=FONT_SMALL,
            height=34,
            command=lambda: self._navigate_to("bookings")
        )
        btn_book.pack(side="left", padx=6)

        btn_search = ctk.CTkButton(
            actions_bar,
            text="🔍 Search Flights",
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_PRIMARY,
            corner_radius=8,
            font=FONT_SMALL,
            height=34,
            command=lambda: self._navigate_to("flights")
        )
        btn_search.pack(side="left", padx=6)

        btn_routes = ctk.CTkButton(
            actions_bar,
            text="🗺 Dijkstra Shortest Route",
            fg_color="#EFF6FF",
            hover_color="#DBEAFE",
            text_color="#1D4ED8",
            corner_radius=8,
            font=FONT_SMALL,
            height=34,
            command=lambda: self._navigate_to("routes")
        )
        btn_routes.pack(side="left", padx=6)

        # ----------------------------------------------------
        # 3. LIVE FLIGHT DEPARTURE STATUS BOARD
        # ----------------------------------------------------
        status_header = ctk.CTkFrame(scrollable, fg_color="transparent")
        status_header.pack(fill="x", pady=(0, 8))

        lbl_status_title = ctk.CTkLabel(
            status_header,
            text="🛫  Live Flight Status & Schedule Board",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_status_title.pack(side="left")

        lbl_simulated_notice = ctk.CTkLabel(
            status_header,
            text="ℹ Displaying real flights from SQLite DB with simulated gate telemetry",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_SECONDARY
        )
        lbl_simulated_notice.pack(side="right")

        # Table columns: Flight No, Route, Departure, Gate, Fare, Seats Left, Status
        columns = [
            ("flight_no", "Flight", 90),
            ("route", "Route (Origin ➔ Destination)", 240),
            ("departure", "Departure", 110),
            ("arrival", "Arrival", 110),
            ("gate", "Terminal / Gate", 120),
            ("fare", "Fare", 90),
            ("seats", "Availability", 110),
            ("status", "Flight Status", 130)
        ]

        self.table_status = ModernTable(
            scrollable,
            columns=columns,
            empty_title="No Flights In Network",
            empty_subtitle="Add flights in Flight Management to view scheduled flight operations.",
            empty_action_text="+ Add New Flight",
            on_empty_action=lambda: self._navigate_to("flights"),
            height=300
        )
        self.table_status.pack(fill="both", expand=True)

        self._populate_flight_status()

    def _populate_flight_status(self):
        flights = self.flight_service.get_all_flights()

        rows = []
        statuses = ["ON TIME", "BOARDING", "DELAYED", "ON TIME"]
        gates = ["Gate A12", "Gate B04", "Gate C02", "Gate A08", "Gate D15"]

        for idx, f in enumerate(flights):
            flight_no, src, dst, dept, arr, total, avail, fare = f
            status = statuses[idx % len(statuses)]
            gate = gates[idx % len(gates)]

            # Formatted airport codes
            src_code = src[:3].upper()
            dst_code = dst[:3].upper()

            rows.append({
                "flight_no": f"SK-{flight_no}",
                "route": f"{src} ({src_code}) ➔ {dst} ({dst_code})",
                "departure": dept or "--:--",
                "arrival": arr or "--:--",
                "gate": gate,
                "fare": f"₹{int(fare):,}",
                "seats": f"{avail} / {total} seats",
                "status": status
            })

        self.table_status.set_data(rows)

    def _navigate_to(self, view_key):
        if self.on_navigate:
            self.on_navigate(view_key)

    def refresh(self):
        flights = self.flight_service.get_all_flights()
        passengers = self.passenger_service.get_all_passengers()
        all_bookings = self.booking_service.get_all_bookings()
        active_bookings_count = sum(1 for b in all_bookings if b[7] == "Confirmed")
        total_revenue = self.revenue_service.calculate_total_revenue()

        self.card_flights.update_value(len(flights))
        self.card_passengers.update_value(len(passengers))
        self.card_bookings.update_value(active_bookings_count)
        self.card_revenue.update_value(total_revenue)

        self._populate_flight_status()
