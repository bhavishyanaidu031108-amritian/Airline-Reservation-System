"""
Waiting List View for SkyLink Airline Reservation System.
Visualizes the Priority Queue data structure, providing queue inspection,
priority additions, and dequeueing (Next Passenger) operations.
"""

import customtkinter as ctk
from services.waiting_list_service import WaitingListService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_STATUS_CANCELLED,
    COLOR_STATUS_ON_TIME, FONT_TITLE, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD,
    FONT_SMALL, FONT_BADGE
)
from GUI.components.dialogs import WaitingListDialog
from GUI.components.tables import ModernTable


class WaitingListView(ctk.CTkFrame):
    def __init__(self, master, user_info=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.waiting_service = WaitingListService()

        # Seed initial sample entries if empty for demonstration
        self._ensure_sample_queue()

        self._build_ui()
        self.load_waiting_list()

    def _ensure_sample_queue(self):
        items = self.waiting_service.get_queue_items()
        if not items:
            self.waiting_service.add_to_waiting_list("P1004", 1)  # High
            self.waiting_service.add_to_waiting_list("P1008", 2)  # Medium
            self.waiting_service.add_to_waiting_list("P1012", 3)  # Low

    def _build_ui(self):
        # ----------------------------------------------------
        # TOP TOOLBAR
        # ----------------------------------------------------
        top_bar = ctk.CTkFrame(self, fg_color="transparent", height=50)
        top_bar.pack(fill="x", pady=(0, 16))

        lbl_title = ctk.CTkLabel(
            top_bar,
            text="⏳  Waiting List (Priority Queue)",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_title.pack(side="left")

        right_controls = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_controls.pack(side="right")

        # Next Passenger Button
        btn_next = ctk.CTkButton(
            right_controls,
            text="Next Passenger  ➔",
            fg_color="#059669",
            hover_color="#047857",
            corner_radius=8,
            font=FONT_SMALL,
            height=36,
            command=self._handle_next_passenger
        )
        btn_next.pack(side="left", padx=(0, 8))

        # Add Passenger Button
        btn_add = ctk.CTkButton(
            right_controls,
            text="+ Add to Waiting List",
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            corner_radius=8,
            font=FONT_SMALL,
            height=36,
            command=self._open_add_dialog
        )
        btn_add.pack(side="left")

        # Notification banner
        self.lbl_notification = ctk.CTkLabel(
            self,
            text="",
            font=FONT_SECTION,
            text_color=COLOR_STATUS_ON_TIME
        )
        self.lbl_notification.pack(anchor="w", pady=(0, 10))

        # Data structure info card
        info_card = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        info_card.pack(fill="x", pady=(0, 16))

        i_row = ctk.CTkFrame(info_card, fg_color="transparent")
        i_row.pack(fill="x", padx=20, pady=12)

        ctk.CTkLabel(i_row, text="💡 Data Structure: Min-Heap Priority Queue", font=FONT_BODY_BOLD, text_color=COLOR_PRIMARY_NAVY).pack(side="left")
        ctk.CTkLabel(i_row, text="Priority 1 = High (Top of Queue)  •  Priority 2 = Medium  •  Priority 3 = Low", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY).pack(side="right")

        # Queue Table
        columns = [
            ("position", "Queue Position", 130),
            ("passenger_id", "Passenger ID", 180),
            ("priority_label", "Priority Tier", 160),
            ("weight", "Heap Weight", 120),
            ("status", "Queue Status", 140)
        ]

        self.table = ModernTable(
            self,
            columns=columns,
            empty_title="Waiting List Empty",
            empty_subtitle="No passengers currently waiting for ticket openings.",
            empty_action_text="+ Add Passenger",
            on_empty_action=self._open_add_dialog
        )
        self.table.pack(fill="both", expand=True)

    def load_waiting_list(self):
        queue_items = self.waiting_service.get_queue_items()

        rows = []
        for index, (priority, passenger_id) in enumerate(queue_items, start=1):
            if priority == 1:
                p_label = "High"
            elif priority == 2:
                p_label = "Medium"
            else:
                p_label = "Low"

            rows.append({
                "position": f"#{index}",
                "passenger_id": str(passenger_id),
                "priority_label": p_label,
                "weight": f"Level {priority}",
                "status": "WAITING"
            })

        self.table.set_data(rows)

    def _open_add_dialog(self):
        def _save(pid, priority):
            self.waiting_service.add_to_waiting_list(pid, priority)
            self.lbl_notification.configure(
                text=f"✓ Added Passenger {pid} to waiting list (Priority {priority}).",
                text_color=COLOR_STATUS_ON_TIME
            )
            self.load_waiting_list()

        WaitingListDialog(self, on_save=_save)

    def _handle_next_passenger(self):
        popped = self.waiting_service.get_next_passenger()
        if popped is None:
            self.lbl_notification.configure(
                text="The waiting list is currently empty.",
                text_color=COLOR_STATUS_CANCELLED
            )
            return

        priority, passenger_id = popped
        prio_name = "High" if priority == 1 else ("Medium" if priority == 2 else "Low")
        self.lbl_notification.configure(
            text=f"✓ Dequeued Next Passenger: {passenger_id} (Priority: {prio_name}) - Assigning available seat!",
            text_color="#059669"
        )
        self.load_waiting_list()
