"""
Modal dialogs and notification toasts for SkyLink Airline Reservation System.
Handles Add/Edit Flight, Add Passenger, Add to Waiting List, and Confirmations.
"""

import customtkinter as ctk
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_STATUS_CANCELLED,
    COLOR_STATUS_ON_TIME, FONT_TITLE, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL
)


class FlightDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Add Flight", initial_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x560")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_CARD)
        self.transient(parent)
        self.grab_set()

        self.initial_data = initial_data or {}
        self.on_save = on_save

        self._build_ui(title)
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 280
        self.geometry(f"+{x}+{y}")

    def _build_ui(self, title):
        # Header
        lbl_header = ctk.CTkLabel(
            self,
            text=f"✈  {title}",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_header.pack(anchor="w", padx=24, pady=(20, 16))

        self.entries = {}

        fields = [
            ("flight_number", "Flight Number", self.initial_data.get("flight_number", "")),
            ("source", "Source Airport (e.g. Hyderabad)", self.initial_data.get("source", "")),
            ("destination", "Destination Airport (e.g. Chennai)", self.initial_data.get("destination", "")),
            ("departure_time", "Departure Time (e.g. 10:00 AM)", self.initial_data.get("departure_time", "")),
            ("arrival_time", "Arrival Time (e.g. 11:30 AM)", self.initial_data.get("arrival_time", "")),
            ("total_seats", "Total Seats", self.initial_data.get("total_seats", "100")),
            ("fare", "Fare (₹)", self.initial_data.get("fare", "4500"))
        ]

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=24)

        for key, label, val in fields:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)

            lbl = ctk.CTkLabel(row, text=label, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY, anchor="w")
            lbl.pack(anchor="w")

            entry = ctk.CTkEntry(
                row,
                height=34,
                corner_radius=8,
                border_color=COLOR_BORDER,
                font=FONT_BODY
            )
            if val:
                entry.insert(0, str(val))
            if key == "flight_number" and self.initial_data.get("flight_number"):
                entry.configure(state="disabled")  # Primary key disabled in edit mode
            entry.pack(fill="x", pady=(2, 0))
            self.entries[key] = entry

        # Error label
        self.lbl_error = ctk.CTkLabel(self, text="", font=FONT_SMALL, text_color=COLOR_STATUS_CANCELLED)
        self.lbl_error.pack(pady=4)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=24, pady=(0, 20))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=100,
            height=36,
            corner_radius=8,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_PRIMARY,
            command=self.destroy
        )
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_submit = ctk.CTkButton(
            btn_frame,
            text="Save Flight",
            width=120,
            height=36,
            corner_radius=8,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._handle_save
        )
        btn_submit.pack(side="right")

    def _handle_save(self):
        try:
            fn = int(self.entries["flight_number"].get().strip())
            src = self.entries["source"].get().strip()
            dst = self.entries["destination"].get().strip()
            dept = self.entries["departure_time"].get().strip()
            arr = self.entries["arrival_time"].get().strip()
            seats = int(self.entries["total_seats"].get().strip())
            fare = float(self.entries["fare"].get().strip())

            if not src or not dst:
                self.lbl_error.configure(text="Source and Destination are required.")
                return

            data = {
                "flight_number": fn,
                "source": src,
                "destination": dst,
                "departure_time": dept,
                "arrival_time": arr,
                "total_seats": seats,
                "available_seats": self.initial_data.get("available_seats", seats),
                "fare": fare
            }

            if self.on_save:
                self.on_save(data)
            self.destroy()
        except ValueError:
            self.lbl_error.configure(text="Please enter valid numbers for Flight No, Seats, and Fare.")


class PassengerDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Add Passenger", initial_data=None, on_save=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x420")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_CARD)
        self.transient(parent)
        self.grab_set()

        self.initial_data = initial_data or {}
        self.on_save = on_save

        self._build_ui(title)
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 225
        y = (self.winfo_screenheight() // 2) - 210
        self.geometry(f"+{x}+{y}")

    def _build_ui(self, title):
        lbl_header = ctk.CTkLabel(
            self,
            text=f"👤  {title}",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_header.pack(anchor="w", padx=24, pady=(20, 16))

        self.entries = {}
        fields = [
            ("passenger_id", "Passenger ID (e.g. 1003)", self.initial_data.get("passenger_id", "")),
            ("name", "Full Name", self.initial_data.get("name", "")),
            ("phone", "Phone Number", self.initial_data.get("phone", "")),
            ("email", "Email Address", self.initial_data.get("email", ""))
        ]

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=24)

        for key, label, val in fields:
            row = ctk.CTkFrame(form_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)

            lbl = ctk.CTkLabel(row, text=label, font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY, anchor="w")
            lbl.pack(anchor="w")

            entry = ctk.CTkEntry(row, height=34, corner_radius=8, border_color=COLOR_BORDER, font=FONT_BODY)
            if val:
                entry.insert(0, str(val))
            if key == "passenger_id" and self.initial_data.get("passenger_id"):
                entry.configure(state="disabled")
            entry.pack(fill="x", pady=(2, 0))
            self.entries[key] = entry

        self.lbl_error = ctk.CTkLabel(self, text="", font=FONT_SMALL, text_color=COLOR_STATUS_CANCELLED)
        self.lbl_error.pack(pady=4)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=24, pady=(0, 20))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=90,
            height=36,
            corner_radius=8,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_PRIMARY,
            command=self.destroy
        )
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_submit = ctk.CTkButton(
            btn_frame,
            text="Save Passenger",
            width=130,
            height=36,
            corner_radius=8,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._handle_save
        )
        btn_submit.pack(side="right")

    def _handle_save(self):
        try:
            pid = int(self.entries["passenger_id"].get().strip())
            name = self.entries["name"].get().strip()
            phone = self.entries["phone"].get().strip()
            email = self.entries["email"].get().strip()

            if not name:
                self.lbl_error.configure(text="Passenger name is required.")
                return

            if self.on_save:
                self.on_save({"passenger_id": pid, "name": name, "phone": phone, "email": email})
            self.destroy()
        except ValueError:
            self.lbl_error.configure(text="Passenger ID must be a numeric integer.")


class WaitingListDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.title("Add to Waiting List")
        self.geometry("400x320")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_CARD)
        self.transient(parent)
        self.grab_set()

        self.on_save = on_save
        self._build_ui()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 200
        y = (self.winfo_screenheight() // 2) - 160
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        lbl_header = ctk.CTkLabel(
            self,
            text="⏳  Add to Waiting List",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_header.pack(anchor="w", padx=24, pady=(20, 16))

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=24)

        lbl_id = ctk.CTkLabel(form_frame, text="Passenger ID (e.g. P1004 or 1004)", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY, anchor="w")
        lbl_id.pack(anchor="w")
        self.entry_id = ctk.CTkEntry(form_frame, height=34, corner_radius=8, border_color=COLOR_BORDER, font=FONT_BODY)
        self.entry_id.pack(fill="x", pady=(2, 10))

        lbl_prio = ctk.CTkLabel(form_frame, text="Priority Level (Priority Queue ordering)", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY, anchor="w")
        lbl_prio.pack(anchor="w")
        self.combo_priority = ctk.CTkComboBox(
            form_frame,
            values=["1 - High Priority", "2 - Medium Priority", "3 - Low Priority"],
            height=34,
            corner_radius=8,
            border_color=COLOR_BORDER,
            font=FONT_BODY
        )
        self.combo_priority.set("1 - High Priority")
        self.combo_priority.pack(fill="x", pady=(2, 10))

        self.lbl_error = ctk.CTkLabel(self, text="", font=FONT_SMALL, text_color=COLOR_STATUS_CANCELLED)
        self.lbl_error.pack(pady=4)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=24, pady=(0, 20))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=90,
            height=36,
            corner_radius=8,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_PRIMARY,
            command=self.destroy
        )
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_submit = ctk.CTkButton(
            btn_frame,
            text="Add Passenger",
            width=130,
            height=36,
            corner_radius=8,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._handle_save
        )
        btn_submit.pack(side="right")

    def _handle_save(self):
        pid = self.entry_id.get().strip()
        if not pid:
            self.lbl_error.configure(text="Passenger ID is required.")
            return

        prio_str = self.combo_priority.get()
        priority = int(prio_str.split(" - ")[0])

        if self.on_save:
            self.on_save(pid, priority)
        self.destroy()


class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Confirm Action", message="Are you sure you want to proceed?", on_confirm=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x220")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_CARD)
        self.transient(parent)
        self.grab_set()

        self.on_confirm = on_confirm
        self._build_ui(title, message)
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 210
        y = (self.winfo_screenheight() // 2) - 110
        self.geometry(f"+{x}+{y}")

    def _build_ui(self, title, message):
        lbl_title = ctk.CTkLabel(
            self,
            text=f"⚠️  {title}",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_title.pack(anchor="w", padx=24, pady=(24, 8))

        lbl_msg = ctk.CTkLabel(
            self,
            text=message,
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            wraplength=370,
            justify="left"
        )
        lbl_msg.pack(anchor="w", padx=24, pady=(0, 24))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=24, pady=(0, 20))

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="No, Cancel",
            width=100,
            height=36,
            corner_radius=8,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_PRIMARY,
            command=self.destroy
        )
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_confirm = ctk.CTkButton(
            btn_frame,
            text="Yes, Confirm",
            width=120,
            height=36,
            corner_radius=8,
            fg_color=COLOR_STATUS_CANCELLED,
            hover_color="#DC2626",
            command=self._handle_confirm
        )
        btn_confirm.pack(side="right")

    def _handle_confirm(self):
        if self.on_confirm:
            self.on_confirm()
        self.destroy()
