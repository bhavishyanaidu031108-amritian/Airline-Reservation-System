"""
Flight Management View for SkyLink Airline Reservation System.
Provides flight CRUD operations, search filters, interactive table,
and modal dialogs directly connected to FlightService and AVL Tree.
"""

import customtkinter as ctk
from services.flight_service import FlightService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, FONT_TITLE, FONT_SECTION,
    FONT_BODY, FONT_SMALL
)
from GUI.components.tables import ModernTable
from GUI.components.dialogs import FlightDialog, ConfirmDialog


class FlightView(ctk.CTkFrame):
    def __init__(self, master, user_info=None, on_book_flight=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.on_book_flight = on_book_flight
        self.flight_service = FlightService()

        self._build_ui()
        self.load_flights()

    def _build_ui(self):
        # ----------------------------------------------------
        # TOP TOOLBAR: Title, Search Input, + Add Flight Button
        # ----------------------------------------------------
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=50)
        top_bar.pack(fill="x", pady=(0, 16))

        # Title
        lbl_title = ctk.CTkLabel(
            top_bar,
            text="🛫  Flight Management",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_title.pack(side="left")

        # Right Toolbar Controls
        right_controls = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_controls.pack(side="right")

        # Search box
        self.entry_search = ctk.CTkEntry(
            right_controls,
            placeholder_text="Search by Flight No, Origin, Destination...",
            width=260,
            height=36,
            corner_radius=8,
            font=FONT_SMALL
        )
        self.entry_search.pack(side="left", padx=(0, 8))
        self.entry_search.bind("<KeyRelease>", lambda e: self._on_search_change())

        # Add Flight Button (Admin only)
        if self.user_info.get("role") == "Admin":
            btn_add = ctk.CTkButton(
                right_controls,
                text="+ Add Flight",
                fg_color=COLOR_SECONDARY_BLUE,
                hover_color="#1D4ED8",
                corner_radius=8,
                font=FONT_SMALL,
                height=36,
                command=self._open_add_flight_dialog
            )
            btn_add.pack(side="left")

        # ----------------------------------------------------
        # FLIGHT TABLE
        # ----------------------------------------------------
        columns = [
            ("flight_no", "Flight No", 90),
            ("source", "Source", 120),
            ("destination", "Destination", 120),
            ("departure", "Departure", 100),
            ("arrival", "Arrival", 100),
            ("seats", "Total Seats", 90),
            ("available", "Available", 90),
            ("fare", "Fare", 90),
            ("status", "Status", 110),
            ("actions", "Actions", 100)
        ]

        self.table = ModernTable(
            self,
            columns=columns,
            empty_title="No Flights Found",
            empty_subtitle="Add a flight to begin managing your flight network.",
            empty_action_text="+ Add Flight" if self.user_info.get("role") == "Admin" else None,
            on_empty_action=self._open_add_flight_dialog
        )
        self.table.pack(fill="both", expand=True)

    def load_flights(self, filter_text=""):
        flights = self.flight_service.get_all_flights()

        rows = []
        term = filter_text.lower().strip()

        for f in flights:
            fn, src, dst, dept, arr, total, avail, fare = f

            # Filtering
            if term:
                match_fn = term in str(fn)
                match_src = term in src.lower()
                match_dst = term in dst.lower()
                if not (match_fn or match_src or match_dst):
                    continue

            status = "AVAILABLE" if avail > 0 else "CANCELLED"

            rows.append({
                "flight_no": str(fn),
                "source": src,
                "destination": dst,
                "departure": dept or "--:--",
                "arrival": arr or "--:--",
                "seats": str(total),
                "available": str(avail),
                "fare": f"₹{int(fare):,}",
                "status": status,
                "raw_flight": f
            })

        self.table.set_data(rows, actions_callback=self._handle_action)

    def _on_search_change(self):
        query = self.entry_search.get()
        self.load_flights(query)

    def _handle_action(self, action_type, row_data):
        raw = row_data.get("raw_flight")
        if not raw:
            return

        flight_no = raw[0]

        if action_type == "view":
            self._show_flight_info(raw)
        elif action_type == "edit":
            if self.user_info.get("role") != "Admin":
                return
            self._open_edit_flight_dialog(raw)
        elif action_type == "delete":
            if self.user_info.get("role") != "Admin":
                return
            self._confirm_delete_flight(flight_no)

    def _show_flight_info(self, flight):
        fn, src, dst, dept, arr, total, avail, fare = flight
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Flight SK-{fn} Details")
        dialog.geometry("400x340")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        card = ctk.CTkFrame(dialog, fg_color=COLOR_BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text=f"✈  Flight {fn}", font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack(pady=(10, 4))
        ctk.CTkLabel(card, text=f"{src} ➔ {dst}", font=FONT_SECTION, text_color=COLOR_SECONDARY_BLUE).pack(pady=(0, 14))

        details = [
            ("Departure:", dept or "--:--"),
            ("Arrival:", arr or "--:--"),
            ("Total Seats:", str(total)),
            ("Available Seats:", str(avail)),
            ("Standard Fare:", f"₹{fare:,.2f}")
        ]

        for label, val in details:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=3)
            ctk.CTkLabel(row, text=label, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(row, text=val, font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY).pack(side="right")

        btn_close = ctk.CTkButton(card, text="Close", width=100, height=32, corner_radius=8, command=dialog.destroy)
        btn_close.pack(pady=(16, 0))

    def _open_add_flight_dialog(self):
        def _save(data):
            self.flight_service.add_flight(
                flight_number=data["flight_number"],
                source=data["source"],
                destination=data["destination"],
                departure_time=data["departure_time"],
                arrival_time=data["arrival_time"],
                total_seats=data["total_seats"],
                available_seats=data["available_seats"],
                fare=data["fare"]
            )
            self.load_flights()

        FlightDialog(self, title="Add New Flight", on_save=_save)

    def _open_edit_flight_dialog(self, raw):
        fn, src, dst, dept, arr, total, avail, fare = raw
        initial = {
            "flight_number": fn,
            "source": src,
            "destination": dst,
            "departure_time": dept,
            "arrival_time": arr,
            "total_seats": total,
            "available_seats": avail,
            "fare": fare
        }

        def _save(data):
            self.flight_service.update_flight(
                flight_number=data["flight_number"],
                source=data["source"],
                destination=data["destination"],
                departure_time=data["departure_time"],
                arrival_time=data["arrival_time"],
                total_seats=data["total_seats"],
                available_seats=data["available_seats"],
                fare=data["fare"]
            )
            self.load_flights()

        FlightDialog(self, title="Edit Flight", initial_data=initial, on_save=_save)

    def _confirm_delete_flight(self, flight_no):
        def _delete():
            self.flight_service.delete_flight(flight_no)
            self.load_flights()

        ConfirmDialog(
            self,
            title="Delete Flight",
            message=f"Are you sure you want to delete flight #{flight_no}? This operation cannot be undone.",
            on_confirm=_delete
        )
