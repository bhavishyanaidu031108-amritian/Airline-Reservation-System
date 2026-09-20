"""
Ticket Cancellation View for SkyLink Airline Reservation System.
Searches bookings via AVL Tree, displays ticket preview card, and executes
safe cancellations via BookingService, restoring flight seat availability.
"""

import customtkinter as ctk
from services.booking_service import BookingService
from services.flight_service import FlightService
from services.passenger_service import PassengerService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_STATUS_CANCELLED, COLOR_STATUS_ON_TIME, COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY, FONT_HERO, FONT_TITLE, FONT_SECTION, FONT_BODY,
    FONT_BODY_BOLD, FONT_SMALL
)
from GUI.components.dialogs import ConfirmDialog
from GUI.components.tables import ModernTable


class CancellationView(ctk.CTkFrame):
    def __init__(self, master, user_info=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.booking_service = BookingService()
        self.flight_service = FlightService()
        self.passenger_service = PassengerService()

        self.current_found_booking = None

        self._build_ui()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        # ----------------------------------------------------
        # SEARCH BY BOOKING ID CARD
        # ----------------------------------------------------
        search_card = ctk.CTkFrame(
            scroll,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        search_card.pack(fill="x", pady=(0, 20))

        s_inner = ctk.CTkFrame(search_card, fg_color="transparent")
        s_inner.pack(fill="x", padx=24, pady=24)

        ctk.CTkLabel(
            s_inner,
            text="❌  Ticket Cancellation Portal",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(anchor="w")

        ctk.CTkLabel(
            s_inner,
            text="Search active reservations by Booking ID using AVL Tree index.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY
        ).pack(anchor="w", pady=(2, 16))

        # Input Row
        row = ctk.CTkFrame(s_inner, fg_color="transparent")
        row.pack(fill="x")

        self.entry_bid = ctk.CTkEntry(
            row,
            placeholder_text="Enter Booking ID (e.g. 5002)",
            width=260,
            height=40,
            corner_radius=8,
            font=FONT_BODY
        )
        self.entry_bid.pack(side="left", padx=(0, 10))

        btn_lookup = ctk.CTkButton(
            row,
            text="Lookup Ticket  🔍",
            height=40,
            corner_radius=8,
            font=FONT_BODY_BOLD,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._handle_lookup
        )
        btn_lookup.pack(side="left")

        # ----------------------------------------------------
        # TICKET PREVIEW CARD (Dynamically populated)
        # ----------------------------------------------------
        self.preview_container = ctk.CTkFrame(scroll, fg_color="transparent")
        self.preview_container.pack(fill="x", pady=(0, 20))

        # Status notification banner
        self.lbl_notification = ctk.CTkLabel(
            scroll,
            text="",
            font=FONT_SECTION,
            text_color=COLOR_STATUS_CANCELLED
        )
        self.lbl_notification.pack(anchor="w", pady=(0, 10))

        # ----------------------------------------------------
        # RECENT BOOKINGS TABLE FOR QUICK PICK
        # ----------------------------------------------------
        ctk.CTkLabel(
            scroll,
            text="📋  All Current Reservations (Click to auto-fill Booking ID)",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(anchor="w", pady=(10, 8))

        columns = [
            ("booking_id", "Booking ID", 110),
            ("passenger", "Passenger Name", 160),
            ("flight_no", "Flight", 90),
            ("route", "Route", 200),
            ("seat", "Seat", 80),
            ("fare", "Fare", 90),
            ("status", "Status", 120)
        ]

        self.table_all = ModernTable(
            scroll,
            columns=columns,
            empty_title="No Bookings in System",
            empty_subtitle="Bookings will show here once created.",
            height=240
        )
        self.table_all.pack(fill="both", expand=True)

        self._load_table()

    def _handle_lookup(self):
        bid_str = self.entry_bid.get().strip().replace("#", "")
        self.lbl_notification.configure(text="")

        if not bid_str:
            self.lbl_notification.configure(text="Please enter a numeric Booking ID.", text_color=COLOR_STATUS_CANCELLED)
            return

        try:
            bid = int(bid_str)
        except ValueError:
            self.lbl_notification.configure(text="Booking ID must be an integer.", text_color=COLOR_STATUS_CANCELLED)
            return

        # Search via AVL Tree
        booking = self.booking_service.search_booking(bid)

        # If not found in active AVL tree, check database if it was already cancelled
        if booking is None:
            all_b = self.booking_service.get_all_bookings()
            match = [b for b in all_b if b[0] == bid]
            if match:
                self._render_preview_card(match[0], is_avl_active=False)
                self.lbl_notification.configure(
                    text=f"ℹ Booking #{bid} exists in database but has already been CANCELLED.",
                    text_color="#F59E0B"
                )
            else:
                self._clear_preview()
                self.lbl_notification.configure(
                    text=f"Booking #{bid} not found in database or AVL tree.",
                    text_color=COLOR_STATUS_CANCELLED
                )
            return

        self._render_preview_card(booking, is_avl_active=True)

    def _render_preview_card(self, booking, is_avl_active):
        self._clear_preview()

        # booking tuple: (booking_id, passenger_id, flight_number, seat_number, booking_status, fare)
        # or from DB join: (b_id, p_id, p_name, f_num, src, dst, seat, status, fare)
        if len(booking) == 6:
            b_id, p_id, f_num, seat, status, fare = booking
            p_data = self.passenger_service.search_passenger(p_id)
            p_name = p_data[1] if p_data else f"Passenger #{p_id}"
            f_data = self.flight_service.search_flight(f_num)
            route = f"{f_data[1]} ➔ {f_data[2]}" if f_data else "Scheduled Flight"
        else:
            b_id, p_id, p_name, f_num, src, dst, seat, status, fare = booking
            route = f"{src} ➔ {dst}"

        self.current_found_booking = b_id

        card = ctk.CTkFrame(
            self.preview_container,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1.5,
            border_color=COLOR_BORDER
        )
        card.pack(fill="x", padx=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24, pady=20)

        # Header Row
        h_row = ctk.CTkFrame(inner, fg_color="transparent")
        h_row.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            h_row,
            text=f"🎫  Booking Details #{b_id}",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(side="left")

        # Status badge
        badge_bg = "#DCFCE7" if status == "Confirmed" else "#FEE2E2"
        badge_fg = "#15803D" if status == "Confirmed" else "#B91C1C"
        badge = ctk.CTkFrame(h_row, fg_color=badge_bg, corner_radius=12, height=26)
        badge.pack(side="right")
        ctk.CTkLabel(badge, text=f"● {status.upper()}", font=FONT_BADGE, text_color=badge_fg, padx=12, pady=4).pack()

        # Grid of fields
        details = [
            ("Passenger Name:", p_name),
            ("Passenger ID:", f"#{p_id}"),
            ("Flight Number:", f"SK-{f_num}"),
            ("Flight Route:", route),
            ("Seat Assignment:", seat or "Unassigned"),
            ("Ticket Fare:", f"₹{fare:,.2f}")
        ]

        grid = ctk.CTkFrame(inner, fg_color="#F8FAFC", corner_radius=10)
        grid.pack(fill="x", pady=(0, 16))

        for label, val in details:
            r = ctk.CTkFrame(grid, fg_color="transparent")
            r.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(r, text=label, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(r, text=val, font=FONT_BODY_BOLD, text_color=COLOR_TEXT_PRIMARY).pack(side="right")

        # Cancel button
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x")

        if is_avl_active and status == "Confirmed":
            btn_cancel = ctk.CTkButton(
                btn_row,
                text="Cancel Ticket & Release Seat  ❌",
                height=40,
                corner_radius=8,
                font=FONT_BODY_BOLD,
                fg_color=COLOR_STATUS_CANCELLED,
                hover_color="#DC2626",
                command=lambda: self._confirm_cancellation(b_id)
            )
            btn_cancel.pack(side="right")
        else:
            ctk.CTkLabel(
                btn_row,
                text="This ticket is already cancelled.",
                font=FONT_SMALL,
                text_color=COLOR_STATUS_CANCELLED
            ).pack(side="right")

    def _clear_preview(self):
        for child in self.preview_container.winfo_children():
            child.destroy()

    def _confirm_cancellation(self, booking_id):
        def _execute_cancel():
            success = self.booking_service.cancel_booking(booking_id)
            if success:
                self.lbl_notification.configure(
                    text=f"✓ Ticket #{booking_id} Cancelled Successfully. Seat restored to flight availability.",
                    text_color=COLOR_STATUS_ON_TIME
                )
                self._clear_preview()
                self._load_table()
            else:
                self.lbl_notification.configure(
                    text=f"Could not cancel booking #{booking_id}.",
                    text_color=COLOR_STATUS_CANCELLED
                )

        ConfirmDialog(
            self,
            title="Cancel Booking",
            message=f"Are you sure you want to cancel Booking #{booking_id}? The seat will be released and the AVL tree record updated.",
            on_confirm=_execute_cancel
        )

    def _load_table(self):
        bookings = self.booking_service.get_all_bookings()
        rows = []
        for b in bookings:
            b_id, p_id, p_name, f_num, src, dst, seat, status, fare = b
            rows.append({
                "booking_id": f"#{b_id}",
                "passenger": f"{p_name or 'ID ' + str(p_id)}",
                "flight_no": f"SK-{f_num}",
                "route": f"{src} ➔ {dst}",
                "seat": seat or "--",
                "fare": f"₹{fare:,.0f}",
                "status": status
            })
        self.table_all.set_data(rows)
