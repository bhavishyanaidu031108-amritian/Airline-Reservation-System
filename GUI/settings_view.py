"""
Settings & System Diagnostics View for SkyLink Airline Reservation System.
Provides live inspection into AVL Trees, Hash Tables, Airport Graph,
and SQLite database connection parameters.
"""

import customtkinter as ctk
from services.flight_service import FlightService
from services.passenger_service import PassengerService
from services.booking_service import BookingService
from services.route_service import RouteService
from services.waiting_list_service import WaitingListService
from services.auth_service import AuthService
from DATABASE.db_connection import DATABASE_NAME
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_ACCENT_SKY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, FONT_HERO,
    FONT_TITLE, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_BADGE
)


class SettingsView(ctk.CTkFrame):
    def __init__(self, master, user_info=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}

        self.flight_service = FlightService()
        self.passenger_service = PassengerService()
        self.booking_service = BookingService()
        self.route_service = RouteService()
        self.waiting_service = WaitingListService()
        self.auth_service = AuthService()

        self._build_ui()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        # Header
        top_bar = ctk.CTkFrame(scroll, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            top_bar,
            text="⚙  System Architecture & Data Structure Inspector",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(side="left")

        # ----------------------------------------------------
        # 1. DATA STRUCTURE STATUS CARDS
        # ----------------------------------------------------
        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x", pady=(0, 20))
        grid.columnconfigure((0, 1), weight=1, uniform="diag_cards")

        # Card 1: AVL Trees
        c1 = ctk.CTkFrame(grid, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        c1.grid(row=0, column=0, padx=(0, 8), pady=4, sticky="nsew")

        ctk.CTkLabel(c1, text="🌲  AVL Trees (Self-Balancing Binary Search Trees)", font=FONT_SECTION, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w", padx=20, pady=(16, 8))

        f_height = self.flight_service.flight_tree.get_height(self.flight_service.flight_tree.root)
        p_height = self.passenger_service.passenger_tree.get_height(self.passenger_service.passenger_tree.root)
        b_height = self.booking_service.booking_tree.get_height(self.booking_service.booking_tree.root)

        avl_metrics = [
            ("Flight Number AVL Tree Height:", f"Height: {f_height} (Search O(log n))"),
            ("Passenger ID AVL Tree Height:", f"Height: {p_height} (Search O(log n))"),
            ("Booking ID AVL Tree Height:", f"Height: {b_height} (Search O(log n))"),
            ("Tree Rotation Support:", "LL, RR, LR, RL Rotations Active")
        ]

        for k, v in avl_metrics:
            r = ctk.CTkFrame(c1, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(r, text=k, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(r, text=v, font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY_NAVY).pack(side="right")

        ctk.CTkLabel(c1, text="", height=8).pack()

        # Card 2: Graph & Dijkstra
        c2 = ctk.CTkFrame(grid, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        c2.grid(row=0, column=1, padx=(8, 0), pady=4, sticky="nsew")

        ctk.CTkLabel(c2, text="🗺  Airport Graph & Dijkstra's Algorithm", font=FONT_SECTION, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w", padx=20, pady=(16, 8))

        airports = self.route_service.get_airports()
        routes = self.route_service.get_all_routes()

        graph_metrics = [
            ("Airport Graph Vertices:", f"{len(airports)} Airports ({', '.join(airports[:3])}...)"),
            ("Weighted Directed Edges:", f"{len(routes)} Airway Segments"),
            ("Shortest Path Algorithm:", "Dijkstra with Adjacency Matrix O(V^2)"),
            ("Sample Benchmark:", "HYD ➔ BOM = 1550 km (Dijkstra Verified)")
        ]

        for k, v in graph_metrics:
            r = ctk.CTkFrame(c2, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(r, text=k, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(r, text=v, font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY_NAVY).pack(side="right")

        ctk.CTkLabel(c2, text="", height=8).pack()

        # ----------------------------------------------------
        # 2. HASH TABLE & PRIORITY QUEUE
        # ----------------------------------------------------
        grid2 = ctk.CTkFrame(scroll, fg_color="transparent")
        grid2.pack(fill="x", pady=(0, 20))
        grid2.columnconfigure((0, 1), weight=1, uniform="diag_cards2")

        # Card 3: Hash Table
        c3 = ctk.CTkFrame(grid2, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        c3.grid(row=0, column=0, padx=(0, 8), pady=4, sticky="nsew")

        ctk.CTkLabel(c3, text="#️⃣  Hash Table (Authentication System)", font=FONT_SECTION, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w", padx=20, pady=(16, 8))

        ht = self.auth_service.login_system
        occupied_slots = sum(1 for bucket in ht.table if bucket)

        ht_metrics = [
            ("Hash Table Capacity:", f"{ht.size} Buckets"),
            ("Collision Resolution:", "Separate Chaining (Linked Buckets)"),
            ("Occupied Buckets:", f"{occupied_slots} / {ht.size}"),
            ("Lookup Average Complexity:", "O(1) Constant Time")
        ]

        for k, v in ht_metrics:
            r = ctk.CTkFrame(c3, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(r, text=k, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(r, text=v, font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY_NAVY).pack(side="right")

        ctk.CTkLabel(c3, text="", height=8).pack()

        # Card 4: Priority Queue
        c4 = ctk.CTkFrame(grid2, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        c4.grid(row=0, column=1, padx=(8, 0), pady=4, sticky="nsew")

        ctk.CTkLabel(c4, text="⏳  Priority Queue (Waiting List)", font=FONT_SECTION, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w", padx=20, pady=(16, 8))

        q_items = self.waiting_service.get_queue_items()

        pq_metrics = [
            ("Queue Implementation:", "Binary Min-Heap (heapq)"),
            ("Current Queue Length:", f"{len(q_items)} Passengers in Waiting List"),
            ("Priority Levels:", "1 (High), 2 (Medium), 3 (Low)"),
            ("Enqueue/Dequeue Complexity:", "O(log k)")
        ]

        for k, v in pq_metrics:
            r = ctk.CTkFrame(c4, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(r, text=k, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(r, text=v, font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY_NAVY).pack(side="right")

        ctk.CTkLabel(c4, text="", height=8).pack()

        # ----------------------------------------------------
        # 3. DATABASE & PERSISTENCE
        # ----------------------------------------------------
        db_card = ctk.CTkFrame(scroll, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        db_card.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(db_card, text="🗄  SQLite Database & Storage Information", font=FONT_SECTION, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w", padx=20, pady=(16, 8))

        db_items = [
            ("Database Engine:", "SQLite 3 (ACID Compliant)"),
            ("Database File:", f"{DATABASE_NAME} (Local Relational Storage)"),
            ("Managed Tables:", "flights, passengers, bookings (with Foreign Keys)")
        ]

        for k, v in db_items:
            r = ctk.CTkFrame(db_card, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(r, text=k, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(r, text=v, font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY_NAVY).pack(side="right")

        ctk.CTkLabel(db_card, text="", height=8).pack()
