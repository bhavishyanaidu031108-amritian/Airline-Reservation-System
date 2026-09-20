"""
Flight Search View for SkyLink Airline Reservation System.
Provides route query panels and renders sleek flight result cards
with direct booking triggers.
"""

from datetime import datetime
import customtkinter as ctk
from services.flight_service import FlightService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_ACCENT_SKY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, FONT_HERO,
    FONT_TITLE, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_BADGE
)


class FlightSearchView(ctk.CTkFrame):
    def __init__(self, master, on_book_flight=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_book_flight = on_book_flight
        self.flight_service = FlightService()

        self._build_ui()
        self._search_flights()  # Initial load with all flights

    def _build_ui(self):
        # ----------------------------------------------------
        # SEARCH HEADER & FILTER PANEL
        # ----------------------------------------------------
        search_card = ctk.CTkFrame(
            self,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        search_card.pack(fill="x", padx=4, pady=(0, 16))

        # Title row
        title_row = ctk.CTkFrame(search_card, fg_color="transparent")
        title_row.pack(fill="x", padx=20, pady=(16, 12))

        ctk.CTkLabel(
            title_row,
            text="🔍  Flight Search & Discovery",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(side="left")

        # Query fields container
        fields_row = ctk.CTkFrame(search_card, fg_color="transparent")
        fields_row.pack(fill="x", padx=20, pady=(0, 20))

        # Distinct airports from database
        all_flights = self.flight_service.get_all_flights()
        sources = sorted(list(set([f[1] for f in all_flights] + ["Hyderabad", "Chennai", "Bangalore", "Mumbai"])))
        destinations = sorted(list(set([f[2] for f in all_flights] + ["Hyderabad", "Chennai", "Bangalore", "Mumbai"])))

        # FROM Field
        from_col = ctk.CTkFrame(fields_row, fg_color="transparent")
        from_col.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkLabel(from_col, text="FROM (ORIGIN)", font=FONT_BADGE, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.combo_from = ctk.CTkComboBox(
            from_col,
            values=["All Sources"] + sources,
            height=38,
            corner_radius=8,
            border_color=COLOR_BORDER,
            font=FONT_BODY
        )
        self.combo_from.set("Hyderabad")
        self.combo_from.pack(fill="x", pady=(4, 0))

        # Swap Button ⇄
        btn_swap = ctk.CTkButton(
            fields_row,
            text="⇄",
            width=36,
            height=36,
            corner_radius=18,
            fg_color="#EFF6FF",
            hover_color="#DBEAFE",
            text_color=COLOR_SECONDARY_BLUE,
            font=("Segoe UI", 16, "bold"),
            command=self._swap_cities
        )
        btn_swap.pack(side="left", padx=4, pady=(18, 0))

        # TO Field
        to_col = ctk.CTkFrame(fields_row, fg_color="transparent")
        to_col.pack(side="left", fill="x", expand=True, padx=(6, 6))
        ctk.CTkLabel(to_col, text="TO (DESTINATION)", font=FONT_BADGE, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.combo_to = ctk.CTkComboBox(
            to_col,
            values=["All Destinations"] + destinations,
            height=38,
            corner_radius=8,
            border_color=COLOR_BORDER,
            font=FONT_BODY
        )
        self.combo_to.set("All Destinations")
        self.combo_to.pack(fill="x", pady=(4, 0))

        # DATE Field
        date_col = ctk.CTkFrame(fields_row, fg_color="transparent")
        date_col.pack(side="left", fill="x", expand=True, padx=(6, 12))
        ctk.CTkLabel(date_col, text="DEPARTURE DATE", font=FONT_BADGE, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.entry_date = ctk.CTkEntry(
            date_col,
            height=38,
            corner_radius=8,
            border_color=COLOR_BORDER,
            font=FONT_BODY
        )
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_date.pack(fill="x", pady=(4, 0))

        # Search Button
        btn_search = ctk.CTkButton(
            fields_row,
            text="Search Flights  ➔",
            width=150,
            height=38,
            corner_radius=8,
            font=FONT_BODY_BOLD,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._search_flights
        )
        btn_search.pack(side="left", pady=(18, 0))

        # ----------------------------------------------------
        # RESULTS SECTION
        # ----------------------------------------------------
        results_header = ctk.CTkFrame(self, fg_color="transparent")
        results_header.pack(fill="x", padx=4, pady=(0, 8))

        self.lbl_results_count = ctk.CTkLabel(
            results_header,
            text="Available Flights",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        )
        self.lbl_results_count.pack(side="left")

        # Scrollable container for cards
        self.results_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_scroll.pack(fill="both", expand=True, padx=4)

    def _swap_cities(self):
        curr_from = self.combo_from.get()
        curr_to = self.combo_to.get()
        self.combo_from.set(curr_to)
        self.combo_to.set(curr_from)

    def _search_flights(self):
        src = self.combo_from.get()
        dst = self.combo_to.get()

        matching = self.flight_service.search_flights_by_route(
            source=None if src == "All Sources" else src,
            destination=None if dst == "All Destinations" else dst
        )

        # Clear existing cards
        for child in self.results_scroll.winfo_children():
            child.destroy()

        self.lbl_results_count.configure(
            text=f"Showing {len(matching)} Available Flight{'s' if len(matching) != 1 else ''}"
        )

        if not matching:
            self._render_empty_search()
            return

        for flight in matching:
            self._render_flight_card(flight)

    def _render_flight_card(self, flight):
        fn, src, dst, dept, arr, total, avail, fare = flight
        src_code = src[:3].upper()
        dst_code = dst[:3].upper()

        card = ctk.CTkFrame(
            self.results_scroll,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER,
            height=110
        )
        card.pack(fill="x", pady=6)
        card.pack_propagate(False)

        # Card hover effect
        def _on_enter(e):
            card.configure(border_color=COLOR_SECONDARY_BLUE, fg_color="#FAFCFF")

        def _on_leave(e):
            card.configure(border_color=COLOR_BORDER, fg_color=COLOR_BG_CARD)

        card.bind("<Enter>", _on_enter)
        card.bind("<Leave>", _on_leave)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="both", expand=True, padx=20, pady=12)

        # 1. Airline & Flight Number
        f_info = ctk.CTkFrame(row, fg_color="transparent", width=120)
        f_info.pack(side="left", fill="y")
        f_info.pack_propagate(False)

        ctk.CTkLabel(f_info, text="✈ SkyLink", font=FONT_BODY_BOLD, text_color=COLOR_SECONDARY_BLUE, anchor="w").pack(anchor="w")
        ctk.CTkLabel(f_info, text=f"Flight SK-{fn}", font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY, anchor="w").pack(anchor="w")
        ctk.CTkLabel(f_info, text="Non-Stop", font=FONT_SMALL, text_color="#10B981", anchor="w").pack(anchor="w")

        # 2. Route Visual (Origin ➔ Destination)
        route_info = ctk.CTkFrame(row, fg_color="transparent")
        route_info.pack(side="left", fill="both", expand=True, padx=20)

        r_top = ctk.CTkFrame(route_info, fg_color="transparent")
        r_top.pack(fill="x", pady=(4, 2))

        # Origin
        o_box = ctk.CTkFrame(r_top, fg_color="transparent")
        o_box.pack(side="left")
        ctk.CTkLabel(o_box, text=src_code, font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w")
        ctk.CTkLabel(o_box, text=src, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")

        # Path arrow
        arrow_box = ctk.CTkFrame(r_top, fg_color="transparent")
        arrow_box.pack(side="left", fill="x", expand=True, padx=16)
        ctk.CTkLabel(arrow_box, text=f"{dept or '10:00 AM'} ─── ✈ ─── {arr or '11:30 AM'}", font=FONT_BODY_BOLD, text_color=COLOR_SECONDARY_BLUE).pack()
        ctk.CTkLabel(arrow_box, text="Scheduled Direct", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack()

        # Destination
        d_box = ctk.CTkFrame(r_top, fg_color="transparent")
        d_box.pack(side="right")
        ctk.CTkLabel(d_box, text=dst_code, font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack(anchor="e")
        ctk.CTkLabel(d_box, text=dst, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="e")

        # 3. Availability & Price & Action Button
        right_box = ctk.CTkFrame(row, fg_color="transparent", width=200)
        right_box.pack(side="right", fill="y")
        right_box.pack_propagate(False)

        # Fare
        ctk.CTkLabel(
            right_box,
            text=f"₹{fare:,.0f}",
            font=FONT_HERO,
            text_color=COLOR_PRIMARY_NAVY,
            anchor="e"
        ).pack(anchor="e")

        # Seats
        ctk.CTkLabel(
            right_box,
            text=f"● {avail} Seats Left",
            font=FONT_SMALL,
            text_color="#10B981" if avail > 10 else "#EF4444",
            anchor="e"
        ).pack(anchor="e", pady=(0, 6))

        # Book Button
        btn_book = ctk.CTkButton(
            right_box,
            text="Book Flight  ➔",
            height=32,
            corner_radius=6,
            font=FONT_SMALL,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=lambda f_data=flight: self._trigger_booking(f_data)
        )
        btn_book.pack(anchor="e")

    def _render_empty_search(self):
        box = ctk.CTkFrame(self.results_scroll, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        box.pack(fill="x", pady=20, padx=20)

        inner = ctk.CTkFrame(box, fg_color="transparent")
        inner.pack(pady=40)

        ctk.CTkLabel(inner, text="✈", font=("Segoe UI", 36), text_color="#94A3B8").pack()
        ctk.CTkLabel(inner, text="No Flights Found on Selected Route", font=FONT_SECTION, text_color=COLOR_PRIMARY_NAVY).pack(pady=(6, 2))
        ctk.CTkLabel(inner, text="Try selecting 'All Sources' or 'All Destinations' to view all available flights.", font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY).pack(pady=(0, 12))

    def _trigger_booking(self, flight_data):
        if self.on_book_flight:
            self.on_book_flight(flight_data)
