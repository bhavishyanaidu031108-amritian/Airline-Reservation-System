"""
Passenger Management View for SkyLink Airline Reservation System.
Provides passenger directory, AVL tree lookups, add/edit/delete modals,
and booking history links.
"""

import customtkinter as ctk
from services.passenger_service import PassengerService
from services.booking_service import BookingService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, FONT_TITLE, FONT_SECTION,
    FONT_BODY, FONT_SMALL
)
from GUI.components.tables import ModernTable
from GUI.components.dialogs import PassengerDialog, ConfirmDialog


class PassengerView(ctk.CTkFrame):
    def __init__(self, master, user_info=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.passenger_service = PassengerService()
        self.booking_service = BookingService()

        self._build_ui()
        self.load_passengers()

    def _build_ui(self):
        # Top toolbar
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=50)
        top_bar.pack(fill="x", pady=(0, 16))

        lbl_title = ctk.CTkLabel(
            top_bar,
            text="👤  Passenger Directory & Management",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_title.pack(side="left")

        right_controls = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_controls.pack(side="right")

        self.entry_search = ctk.CTkEntry(
            right_controls,
            placeholder_text="Search by ID, Name, Phone, Email...",
            width=260,
            height=36,
            corner_radius=8,
            font=FONT_SMALL
        )
        self.entry_search.pack(side="left", padx=(0, 8))
        self.entry_search.bind("<KeyRelease>", lambda e: self._on_search_change())

        if self.user_info.get("role") == "Admin":
            btn_add = ctk.CTkButton(
                right_controls,
                text="+ Add Passenger",
                fg_color=COLOR_SECONDARY_BLUE,
                hover_color="#1D4ED8",
                corner_radius=8,
                font=FONT_SMALL,
                height=36,
                command=self._open_add_passenger_dialog
            )
            btn_add.pack(side="left")

        # Table
        columns = [
            ("passenger_id", "Passenger ID", 110),
            ("name", "Full Name", 180),
            ("phone", "Phone Number", 130),
            ("email", "Email Address", 200),
            ("bookings", "Active Bookings", 120),
            ("status", "Profile Status", 110),
            ("actions", "Actions", 100)
        ]

        self.table = ModernTable(
            self,
            columns=columns,
            empty_title="No Passengers Found",
            empty_subtitle="Register a new passenger to begin managing customer profiles.",
            empty_action_text="+ Add Passenger" if self.user_info.get("role") == "Admin" else None,
            on_empty_action=self._open_add_passenger_dialog
        )
        self.table.pack(fill="both", expand=True)

    def load_passengers(self, filter_text=""):
        passengers = self.passenger_service.get_all_passengers()
        all_bookings = self.booking_service.get_all_bookings()

        # Count active bookings per passenger
        booking_counts = {}
        for b in all_bookings:
            pid = b[1]
            if b[7] == "Confirmed":
                booking_counts[pid] = booking_counts.get(pid, 0) + 1

        rows = []
        term = filter_text.lower().strip()

        for p in passengers:
            pid, name, phone, email = p

            if term:
                match_id = term in str(pid)
                match_name = term in name.lower()
                match_phone = term in str(phone).lower()
                match_email = term in str(email).lower()
                if not (match_id or match_name or match_phone or match_email):
                    continue

            b_count = booking_counts.get(pid, 0)

            rows.append({
                "passenger_id": str(pid),
                "name": name,
                "phone": phone or "N/A",
                "email": email or "N/A",
                "bookings": f"{b_count} Flight{'s' if b_count != 1 else ''}",
                "status": "ACTIVE",
                "raw_passenger": p
            })

        self.table.set_data(rows, actions_callback=self._handle_action)

    def _on_search_change(self):
        query = self.entry_search.get()
        self.load_passengers(query)

    def _handle_action(self, action_type, row_data):
        raw = row_data.get("raw_passenger")
        if not raw:
            return

        pid = raw[0]

        if action_type == "view":
            self._show_passenger_info(raw)
        elif action_type == "edit":
            if self.user_info.get("role") != "Admin":
                return
            self._open_edit_passenger_dialog(raw)
        elif action_type == "delete":
            if self.user_info.get("role") != "Admin":
                return
            self._confirm_delete_passenger(pid)

    def _show_passenger_info(self, p):
        pid, name, phone, email = p
        bookings = self.booking_service.get_passenger_bookings(pid)

        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Passenger Profile - {name}")
        dialog.geometry("440x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        card = ctk.CTkFrame(dialog, fg_color=COLOR_BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="👤", font=("Segoe UI", 32)).pack(pady=(8, 2))
        ctk.CTkLabel(card, text=name, font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack()
        ctk.CTkLabel(card, text=f"Passenger ID: #{pid}", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(pady=(0, 14))

        details = [
            ("Phone:", phone or "Not provided"),
            ("Email:", email or "Not provided"),
            ("Total Bookings:", f"{len(bookings)} Flights"),
        ]

        for label, val in details:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=3)
            ctk.CTkLabel(row, text=label, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(row, text=val, font=FONT_BODY, text_color=COLOR_TEXT_PRIMARY).pack(side="right")

        # Bookings snippet
        if bookings:
            ctk.CTkLabel(card, text="Recent Bookings:", font=FONT_SECTION, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w", padx=24, pady=(12, 4))
            for b in bookings[:3]:
                b_id, _, _, f_num, src, dst, seat, status, fare = b
                b_row = ctk.CTkFrame(card, fg_color="#F8FAFC", corner_radius=6, height=28)
                b_row.pack(fill="x", padx=24, pady=2)
                ctk.CTkLabel(b_row, text=f"#{b_id}: {src} ➔ {dst} (Seat {seat})", font=FONT_SMALL, text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=8)
                ctk.CTkLabel(b_row, text=status, font=FONT_SMALL, text_color="#10B981" if status == "Confirmed" else "#EF4444").pack(side="right", padx=8)

        btn_close = ctk.CTkButton(card, text="Close", width=100, height=32, corner_radius=8, command=dialog.destroy)
        btn_close.pack(pady=(16, 0))

    def _open_add_passenger_dialog(self):
        def _save(data):
            self.passenger_service.add_passenger(
                passenger_id=data["passenger_id"],
                name=data["name"],
                phone=data["phone"],
                email=data["email"]
            )
            self.load_passengers()

        PassengerDialog(self, title="Add New Passenger", on_save=_save)

    def _open_edit_passenger_dialog(self, raw):
        pid, name, phone, email = raw
        initial = {
            "passenger_id": pid,
            "name": name,
            "phone": phone,
            "email": email
        }

        def _save(data):
            self.passenger_service.update_passenger(
                passenger_id=data["passenger_id"],
                name=data["name"],
                phone=data["phone"],
                email=data["email"]
            )
            self.load_passengers()

        PassengerDialog(self, title="Edit Passenger", initial_data=initial, on_save=_save)

    def _confirm_delete_passenger(self, pid):
        def _delete():
            self.passenger_service.delete_passenger(pid)
            self.load_passengers()

        ConfirmDialog(
            self,
            title="Delete Passenger",
            message=f"Are you sure you want to delete passenger profile #{pid}?",
            on_confirm=_delete
        )
