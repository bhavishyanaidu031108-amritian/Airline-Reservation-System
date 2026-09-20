"""
Multi-step Flight Reservation / Booking Wizard for SkyLink.
Features visual progress stepper, passenger selector/input, interactive airplane
cabin seat map, confirmation boarding pass, and direct connection to BookingService.
"""

import random
import customtkinter as ctk
import tkinter as tk
from services.flight_service import FlightService
from services.passenger_service import PassengerService
from services.booking_service import BookingService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_ACCENT_SKY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_WHITE,
    COLOR_STATUS_ON_TIME, COLOR_STATUS_CANCELLED, FONT_HERO, FONT_TITLE,
    FONT_SECTION, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_BADGE
)
from GUI.components.tables import ModernTable


class BookingView(ctk.CTkFrame):
    def __init__(self, master, preselected_flight=None, user_info=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.preselected_flight = preselected_flight

        self.flight_service = FlightService()
        self.passenger_service = PassengerService()
        self.booking_service = BookingService()

        # Wizard state
        self.current_step = 1
        self.selected_flight = None
        self.passenger_data = {}
        self.selected_seat = "A1"
        self.confirmed_booking = None

        self._build_ui()

        if self.preselected_flight:
            self._apply_preselected_flight(self.preselected_flight)

    def _build_ui(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=4, pady=4)

        # ----------------------------------------------------
        # TOP STEP PROGRESS INDICATOR
        # ----------------------------------------------------
        self.stepper_card = ctk.CTkFrame(
            self.scroll,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER,
            height=80
        )
        self.stepper_card.pack(fill="x", pady=(0, 16))
        self.stepper_card.pack_propagate(False)

        self._render_stepper()

        # ----------------------------------------------------
        # STEP CONTENT CONTAINER
        # ----------------------------------------------------
        self.step_container = ctk.CTkFrame(
            self.scroll,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        self.step_container.pack(fill="x", pady=(0, 20))

        # Show initial step
        self._show_step(1)

        # ----------------------------------------------------
        # ALL BOOKINGS DIRECTORY TABLE
        # ----------------------------------------------------
        lbl_history = ctk.CTkLabel(
            self.scroll,
            text="🎫  Recent Reservation Records",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_history.pack(anchor="w", pady=(8, 8))

        columns = [
            ("booking_id", "Booking ID", 110),
            ("passenger", "Passenger", 150),
            ("flight_no", "Flight", 90),
            ("route", "Route", 200),
            ("seat", "Seat", 80),
            ("fare", "Fare", 90),
            ("status", "Booking Status", 120)
        ]

        self.table_bookings = ModernTable(
            self.scroll,
            columns=columns,
            empty_title="No Bookings Recorded",
            empty_subtitle="Confirmed flight reservations will appear here.",
            height=260
        )
        self.table_bookings.pack(fill="both", expand=True)
        self._load_bookings_table()

    def _render_stepper(self):
        for child in self.stepper_card.winfo_children():
            child.destroy()

        step_labels = [
            (1, "Select Flight"),
            (2, "Passenger Details"),
            (3, "Seat Selection"),
            (4, "Confirm & Book")
        ]

        row = ctk.CTkFrame(self.stepper_card, fg_color="transparent")
        row.place(relx=0.5, rely=0.5, anchor="center")

        for idx, (num, title) in enumerate(step_labels):
            is_active = (num == self.current_step)
            is_done = (num < self.current_step)

            # Circle badge
            bg = COLOR_SECONDARY_BLUE if (is_active or is_done) else "#E2E8F0"
            fg = "#FFFFFF" if (is_active or is_done) else "#64748B"
            badge_text = "✓" if is_done else str(num)

            badge = ctk.CTkFrame(row, fg_color=bg, width=28, height=28, corner_radius=14)
            badge.pack(side="left")
            badge.pack_propagate(False)

            ctk.CTkLabel(badge, text=badge_text, font=FONT_BADGE, text_color=fg).place(relx=0.5, rely=0.5, anchor="center")

            # Title
            t_color = COLOR_PRIMARY_NAVY if is_active else ("#10B981" if is_done else "#94A3B8")
            lbl_title = ctk.CTkLabel(row, text=f" {title} ", font=FONT_BODY_BOLD if is_active else FONT_SMALL, text_color=t_color)
            lbl_title.pack(side="left", padx=(4, 12))

            # Connector line
            if idx < len(step_labels) - 1:
                line_color = COLOR_SECONDARY_BLUE if is_done else "#E2E8F0"
                line = ctk.CTkFrame(row, fg_color=line_color, width=40, height=2)
                line.pack(side="left", padx=(0, 12))

    def _show_step(self, step_num):
        self.current_step = step_num
        self._render_stepper()

        for child in self.step_container.winfo_children():
            child.destroy()

        if step_num == 1:
            self._render_step1_select_flight()
        elif step_num == 2:
            self._render_step2_passenger_details()
        elif step_num == 3:
            self._render_step3_seat_selection()
        elif step_num == 4:
            self._render_step4_confirm_booking()
        elif step_num == 5:
            self._render_step5_confirmation_success()

    # ----------------------------------------------------
    # STEP 1: SELECT FLIGHT
    # ----------------------------------------------------
    def _render_step1_select_flight(self):
        f = ctk.CTkFrame(self.step_container, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(f, text="Step 1: Choose Flight Route", font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w")
        ctk.CTkLabel(f, text="Select an available flight schedule for reservation.", font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(2, 16))

        flights = self.flight_service.get_all_flights()
        if not flights:
            ctk.CTkLabel(f, text="No flights scheduled yet.", font=FONT_BODY, text_color=COLOR_STATUS_CANCELLED).pack(anchor="w")
            return

        self.flight_radio_var = tk.IntVar(value=self.selected_flight[0] if self.selected_flight else flights[0][0])

        options_box = ctk.CTkScrollableFrame(f, fg_color="transparent", height=200)
        options_box.pack(fill="x", pady=(0, 16))

        for fl in flights:
            fn, src, dst, dept, arr, total, avail, fare = fl

            card = ctk.CTkFrame(options_box, fg_color="#F8FAFC", corner_radius=8, border_width=1, border_color=COLOR_BORDER)
            card.pack(fill="x", pady=4)

            r_btn = ctk.CTkRadioButton(
                card,
                text=f"Flight SK-{fn}: {src} ➔ {dst}  |  {dept or '10:00 AM'} - {arr or '11:30 AM'}  |  Fare: ₹{fare:,.0f}  |  Available: {avail}/{total} Seats",
                variable=self.flight_radio_var,
                value=fn,
                font=FONT_BODY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_SECONDARY_BLUE
            )
            r_btn.pack(side="left", padx=14, pady=12)

        btn_next = ctk.CTkButton(
            f,
            text="Proceed to Passenger Details  ➔",
            height=38,
            corner_radius=8,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._handle_step1_next
        )
        btn_next.pack(side="right")

    def _handle_step1_next(self):
        fn = self.flight_radio_var.get()
        flight_tuple = self.flight_service.search_flight(fn)
        if flight_tuple:
            self.selected_flight = flight_tuple
            self._show_step(2)

    # ----------------------------------------------------
    # STEP 2: PASSENGER DETAILS
    # ----------------------------------------------------
    def _render_step2_passenger_details(self):
        f = ctk.CTkFrame(self.step_container, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(f, text="Step 2: Passenger Information", font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w")
        ctk.CTkLabel(f, text="Select an existing registered passenger or enter new passenger details.", font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(2, 16))

        # Quick select from registered passengers
        passengers = self.passenger_service.get_all_passengers()
        if passengers:
            p_select_row = ctk.CTkFrame(f, fg_color="#F1F5F9", corner_radius=8, height=44)
            p_select_row.pack(fill="x", pady=(0, 16))
            p_select_row.pack_propagate(False)

            ctk.CTkLabel(p_select_row, text="Select Existing Passenger:", font=FONT_SMALL, text_color=COLOR_TEXT_PRIMARY).pack(side="left", padx=12)

            p_options = [f"#{p[0]} - {p[1]}" for p in passengers]
            self.combo_passengers = ctk.CTkComboBox(
                p_select_row,
                values=["-- Enter Manually --"] + p_options,
                width=240,
                command=self._on_passenger_dropdown_change
            )
            self.combo_passengers.set("-- Enter Manually --")
            self.combo_passengers.pack(side="left", padx=6)

        # Form fields
        form = ctk.CTkFrame(f, fg_color="transparent")
        form.pack(fill="x", pady=(0, 16))

        # Passenger ID
        ctk.CTkLabel(form, text="Passenger ID (Integer)", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.entry_pid = ctk.CTkEntry(form, height=36, corner_radius=8, border_color=COLOR_BORDER)
        self.entry_pid.pack(fill="x", pady=(2, 10))
        # Default next ID
        existing_ids = [p[0] for p in passengers] if passengers else [1000]
        self.entry_pid.insert(0, str(max(existing_ids) + 1 if existing_ids else 1001))

        # Full Name
        ctk.CTkLabel(form, text="Full Name", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.entry_pname = ctk.CTkEntry(form, height=36, corner_radius=8, border_color=COLOR_BORDER)
        self.entry_pname.pack(fill="x", pady=(2, 10))
        self.entry_pname.insert(0, self.user_info.get("username", "Passenger").capitalize())

        # Phone
        ctk.CTkLabel(form, text="Phone Number", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.entry_pphone = ctk.CTkEntry(form, height=36, corner_radius=8, border_color=COLOR_BORDER)
        self.entry_pphone.pack(fill="x", pady=(2, 10))
        self.entry_pphone.insert(0, "9876543210")

        # Email
        ctk.CTkLabel(form, text="Email Address", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.entry_pemail = ctk.CTkEntry(form, height=36, corner_radius=8, border_color=COLOR_BORDER)
        self.entry_pemail.pack(fill="x", pady=(2, 10))
        self.entry_pemail.insert(0, f"{self.user_info.get('username', 'user').lower()}@gmail.com")

        self.lbl_step2_error = ctk.CTkLabel(f, text="", font=FONT_SMALL, text_color=COLOR_STATUS_CANCELLED)
        self.lbl_step2_error.pack(anchor="w", pady=(0, 8))

        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack(fill="x")

        btn_back = ctk.CTkButton(btn_row, text="◀ Back", width=90, height=38, corner_radius=8, fg_color="#F1F5F9", hover_color="#E2E8F0", text_color=COLOR_TEXT_PRIMARY, command=lambda: self._show_step(1))
        btn_back.pack(side="left")

        btn_next = ctk.CTkButton(btn_row, text="Proceed to Seat Selection  ➔", height=38, corner_radius=8, fg_color=COLOR_SECONDARY_BLUE, hover_color="#1D4ED8", command=self._handle_step2_next)
        btn_next.pack(side="right")

    def _on_passenger_dropdown_change(self, choice):
        if choice and choice != "-- Enter Manually --":
            pid_str = choice.split(" - ")[0].replace("#", "")
            p_data = self.passenger_service.search_passenger(int(pid_str))
            if p_data:
                pid, name, phone, email = p_data
                self.entry_pid.delete(0, "end")
                self.entry_pid.insert(0, str(pid))
                self.entry_pname.delete(0, "end")
                self.entry_pname.insert(0, name)
                self.entry_pphone.delete(0, "end")
                self.entry_pphone.insert(0, phone or "")
                self.entry_pemail.delete(0, "end")
                self.entry_pemail.insert(0, email or "")

    def _handle_step2_next(self):
        try:
            pid = int(self.entry_pid.get().strip())
            name = self.entry_pname.get().strip()
            phone = self.entry_pphone.get().strip()
            email = self.entry_pemail.get().strip()

            if not name:
                self.lbl_step2_error.configure(text="Passenger name is required.")
                return

            self.passenger_data = {
                "passenger_id": pid,
                "name": name,
                "phone": phone,
                "email": email
            }

            # Save/ensure passenger is in AVL tree & SQLite DB
            existing = self.passenger_service.search_passenger(pid)
            if not existing:
                self.passenger_service.add_passenger(pid, name, phone, email)

            self._show_step(3)
        except ValueError:
            self.lbl_step2_error.configure(text="Passenger ID must be a valid integer.")

    # ----------------------------------------------------
    # STEP 3: SEAT SELECTION
    # ----------------------------------------------------
    def _render_step3_seat_selection(self):
        f = ctk.CTkFrame(self.step_container, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(f, text="Step 3: Select Cabin Seat", font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w")
        ctk.CTkLabel(f, text=f"Aircraft Boeing 737 • Flight SK-{self.selected_flight[0]} ({self.selected_flight[1]} ➔ {self.selected_flight[2]})", font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(2, 16))

        # Legend
        legend_row = ctk.CTkFrame(f, fg_color="transparent")
        legend_row.pack(fill="x", pady=(0, 14))

        for color, label in [("#EFF6FF", "Available"), (COLOR_SECONDARY_BLUE, "Selected"), ("#E2E8F0", "Occupied")]:
            dot = ctk.CTkFrame(legend_row, fg_color=color, width=16, height=16, corner_radius=4, border_width=1, border_color=COLOR_BORDER)
            dot.pack(side="left", padx=(0, 4))
            ctk.CTkLabel(legend_row, text=label, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left", padx=(0, 16))

        # Cabin fuselage container
        cabin = ctk.CTkFrame(f, fg_color="#F8FAFC", corner_radius=14, border_width=1, border_color=COLOR_BORDER)
        cabin.pack(pady=(0, 16), padx=40)

        # Booked seats from DB
        booked_seats = set(self.booking_service.get_booked_seats_for_flight(self.selected_flight[0]))

        self.seat_buttons = {}
        rows = 8
        columns = ["A", "B", "aisle", "C", "D"]

        # Cockpit header
        ctk.CTkLabel(cabin, text="▲ COCKPIT / FRONT ▲", font=("Segoe UI", 10, "bold"), text_color="#94A3B8").pack(pady=(10, 8))

        grid_frame = ctk.CTkFrame(cabin, fg_color="transparent")
        grid_frame.pack(padx=20, pady=(0, 14))

        for r in range(1, rows + 1):
            row_box = ctk.CTkFrame(grid_frame, fg_color="transparent")
            row_box.pack(pady=3)

            # Row number indicator
            ctk.CTkLabel(row_box, text=str(r), width=20, font=FONT_SMALL, text_color="#94A3B8").pack(side="left", padx=(0, 6))

            for col in columns:
                if col == "aisle":
                    ctk.CTkLabel(row_box, text="", width=24).pack(side="left")
                    continue

                seat_code = f"{col}{r}"
                is_booked = seat_code in booked_seats
                is_selected = (seat_code == self.selected_seat)

                if is_booked:
                    btn_color = "#E2E8F0"
                    text_color = "#94A3B8"
                    state = "disabled"
                elif is_selected:
                    btn_color = COLOR_SECONDARY_BLUE
                    text_color = "#FFFFFF"
                    state = "normal"
                else:
                    btn_color = "#EFF6FF"
                    text_color = COLOR_PRIMARY_NAVY
                    state = "normal"

                btn = ctk.CTkButton(
                    row_box,
                    text=seat_code,
                    width=42,
                    height=36,
                    corner_radius=6,
                    font=FONT_SMALL,
                    fg_color=btn_color,
                    hover_color="#DBEAFE" if not is_booked else "#E2E8F0",
                    text_color=text_color,
                    state=state,
                    command=lambda sc=seat_code: self._select_seat(sc)
                )
                btn.pack(side="left", padx=3)
                self.seat_buttons[seat_code] = (btn, is_booked)

        # Selected seat summary bar
        self.lbl_selected_seat_info = ctk.CTkLabel(
            f,
            text=f"Selected Seat: {self.selected_seat} (Economy Class • Standard Legroom)",
            font=FONT_BODY_BOLD,
            text_color=COLOR_SECONDARY_BLUE
        )
        self.lbl_selected_seat_info.pack(pady=(0, 14))

        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack(fill="x")

        btn_back = ctk.CTkButton(btn_row, text="◀ Back", width=90, height=38, corner_radius=8, fg_color="#F1F5F9", hover_color="#E2E8F0", text_color=COLOR_TEXT_PRIMARY, command=lambda: self._show_step(2))
        btn_back.pack(side="left")

        btn_next = ctk.CTkButton(btn_row, text="Proceed to Confirmation  ➔", height=38, corner_radius=8, fg_color=COLOR_SECONDARY_BLUE, hover_color="#1D4ED8", command=lambda: self._show_step(4))
        btn_next.pack(side="right")

    def _select_seat(self, seat_code):
        self.selected_seat = seat_code
        for sc, (btn, is_booked) in self.seat_buttons.items():
            if is_booked:
                continue
            if sc == seat_code:
                btn.configure(fg_color=COLOR_SECONDARY_BLUE, text_color="#FFFFFF")
            else:
                btn.configure(fg_color="#EFF6FF", text_color=COLOR_PRIMARY_NAVY)
        self.lbl_selected_seat_info.configure(text=f"Selected Seat: {seat_code} (Economy Class • Standard Legroom)")

    # ----------------------------------------------------
    # STEP 4: CONFIRM & BOOK
    # ----------------------------------------------------
    def _render_step4_confirm_booking(self):
        f = ctk.CTkFrame(self.step_container, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(f, text="Step 4: Review & Confirm Booking", font=FONT_TITLE, text_color=COLOR_PRIMARY_NAVY).pack(anchor="w")
        ctk.CTkLabel(f, text="Please review flight reservation details before confirming.", font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", pady=(2, 16))

        # Preview card
        card = ctk.CTkFrame(f, fg_color="#F8FAFC", corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        card.pack(fill="x", pady=(0, 20), padx=20)

        fn, src, dst, dept, arr, _, _, fare = self.selected_flight
        p_name = self.passenger_data.get("name", "Passenger")
        pid = self.passenger_data.get("passenger_id", "N/A")

        items = [
            ("Flight Number:", f"SK-{fn}"),
            ("Route:", f"{src} ➔ {dst}"),
            ("Schedule:", f"{dept or '10:00 AM'} - {arr or '11:30 AM'}"),
            ("Passenger Name:", p_name),
            ("Passenger ID:", f"#{pid}"),
            ("Cabin Seat:", self.selected_seat),
            ("Total Payable Fare:", f"₹{fare:,.2f}"),
            ("Booking Status:", "Confirmed (Upon Confirmation)")
        ]

        for label, val in items:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=4)
            ctk.CTkLabel(row, text=label, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="left")
            ctk.CTkLabel(row, text=val, font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY_NAVY).pack(side="right")

        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack(fill="x")

        btn_back = ctk.CTkButton(btn_row, text="◀ Back", width=90, height=38, corner_radius=8, fg_color="#F1F5F9", hover_color="#E2E8F0", text_color=COLOR_TEXT_PRIMARY, command=lambda: self._show_step(3))
        btn_back.pack(side="left")

        btn_confirm = ctk.CTkButton(
            btn_row,
            text="Confirm & Issue Ticket  ✓",
            height=40,
            corner_radius=8,
            font=FONT_SECTION,
            fg_color="#10B981",
            hover_color="#059669",
            command=self._handle_confirm_booking
        )
        btn_confirm.pack(side="right")

    def _handle_confirm_booking(self):
        # Generate new unique booking ID
        all_b = self.booking_service.get_all_bookings()
        existing_b_ids = [b[0] for b in all_b] if all_b else [5000]
        new_booking_id = max(existing_b_ids) + 1 if existing_b_ids else 5001

        fn, src, dst, dept, arr, _, _, fare = self.selected_flight
        pid = self.passenger_data["passenger_id"]

        # Call existing BookingService method
        self.booking_service.create_booking(
            booking_id=new_booking_id,
            passenger_id=pid,
            flight_number=fn,
            seat_number=self.selected_seat,
            booking_status="Confirmed",
            fare=fare
        )

        self.confirmed_booking = {
            "booking_id": new_booking_id,
            "passenger_id": pid,
            "passenger_name": self.passenger_data["name"],
            "flight_number": fn,
            "source": src,
            "destination": dst,
            "seat_number": self.selected_seat,
            "fare": fare
        }

        self._load_bookings_table()
        self._show_step(5)

    # ----------------------------------------------------
    # STEP 5: CONFIRMATION SUCCESS (BOARDING PASS)
    # ----------------------------------------------------
    def _render_step5_confirmation_success(self):
        f = ctk.CTkFrame(self.step_container, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=24, pady=24)

        b = self.confirmed_booking or {}

        # Success Banner
        success_bar = ctk.CTkFrame(f, fg_color="#ECFDF5", corner_radius=10, border_width=1, border_color="#A7F3D0")
        success_bar.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            success_bar,
            text="✓   BOOKING CONFIRMED & TICKET ISSUED",
            font=FONT_TITLE,
            text_color="#059669",
            padx=20,
            pady=12
        ).pack(side="left")

        # Boarding Pass Card
        pass_card = ctk.CTkFrame(f, fg_color=COLOR_PRIMARY_NAVY, corner_radius=14, height=180)
        pass_card.pack(fill="x", padx=10, pady=(0, 20))
        pass_card.pack_propagate(False)

        p_row = ctk.CTkFrame(pass_card, fg_color="transparent")
        p_row.pack(fill="both", expand=True, padx=24, pady=16)

        # Left ticket details
        t_left = ctk.CTkFrame(p_row, fg_color="transparent")
        t_left.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(t_left, text=f"✈  SKYLINK BOARDING PASS • E-TICKET #{b.get('booking_id')}", font=FONT_BADGE, text_color=COLOR_ACCENT_SKY).pack(anchor="w")
        ctk.CTkLabel(t_left, text=f"{b.get('source')} ➔ {b.get('destination')}", font=FONT_HERO, text_color=COLOR_TEXT_WHITE).pack(anchor="w", pady=(4, 8))

        ctk.CTkLabel(t_left, text=f"Passenger: {b.get('passenger_name')} (ID: #{b.get('passenger_id')})", font=FONT_BODY, text_color="#E2E8F0").pack(anchor="w")
        ctk.CTkLabel(t_left, text=f"Flight: SK-{b.get('flight_number')}  |  Seat: {b.get('seat_number')}  |  Fare: ₹{b.get('fare'):,.0f}", font=FONT_SMALL, text_color="#94A3B8").pack(anchor="w", pady=(2, 0))

        # Right Barcode simulation
        t_right = ctk.CTkFrame(p_row, fg_color="transparent", width=140)
        t_right.pack(side="right", fill="y")
        t_right.pack_propagate(False)

        barcode_canvas = tk.Canvas(t_right, width=130, height=80, bg=COLOR_PRIMARY_NAVY, highlightthickness=0)
        barcode_canvas.pack(pady=10)
        # Draw barcode vertical bars
        for i in range(12, 120, 4):
            w = 2 if i % 8 == 0 else 1
            barcode_canvas.create_line(i, 10, i, 70, fill="#FFFFFF", width=w)

        ctk.CTkLabel(t_right, text="GATE CLOSES 20M PRIOR", font=("Segoe UI", 8, "bold"), text_color=COLOR_ACCENT_SKY).pack()

        # Action Buttons
        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack(fill="x")

        btn_new = ctk.CTkButton(
            btn_row,
            text="+ Book Another Flight",
            height=38,
            corner_radius=8,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=lambda: self._show_step(1)
        )
        btn_new.pack(side="right")

    def _load_bookings_table(self):
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
        self.table_bookings.set_data(rows)

    def _apply_preselected_flight(self, flight):
        self.selected_flight = flight
        self._show_step(2)
