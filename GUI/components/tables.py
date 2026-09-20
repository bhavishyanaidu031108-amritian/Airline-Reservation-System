"""
Modern custom Table component for SkyLink Airline Reservation System.
Features clean typography, alternating rows, hover highlights, status pills,
action buttons, and graceful empty states.
"""

import customtkinter as ctk
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_BG_HOVER, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_MUTED,
    COLOR_STATUS_ON_TIME, COLOR_STATUS_BOARDING, COLOR_STATUS_DELAYED,
    COLOR_STATUS_CANCELLED, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL, FONT_BADGE,
    FONT_SECTION
)


class ModernTable(ctk.CTkFrame):
    def __init__(self, master, columns, empty_title="No Data Available", empty_subtitle="Nothing to display here yet.", empty_action_text=None, on_empty_action=None, **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER,
            **kwargs
        )
        self.columns = columns  # List of tuples: (col_key, col_title, weight/width)
        self.empty_title = empty_title
        self.empty_subtitle = empty_subtitle
        self.empty_action_text = empty_action_text
        self.on_empty_action = on_empty_action

        self._build_header()
        self._build_body_container()

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="#F8FAFC", height=42, corner_radius=8)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 4))
        self.header_frame.pack_propagate(False)

        for col_key, col_title, width in self.columns:
            lbl = ctk.CTkLabel(
                self.header_frame,
                text=col_title.upper(),
                font=FONT_BADGE,
                text_color=COLOR_TEXT_SECONDARY,
                width=width,
                anchor="w"
            )
            lbl.pack(side="left", padx=8)

    def _build_body_container(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=8, pady=(0, 10))

    def set_data(self, rows, actions_callback=None):
        """
        Populate table with rows.
        rows: list of dicts {col_key: value} or lists matching columns.
        actions_callback: function(action_type, row_data)
        """
        # Clear existing rows
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        if not rows:
            self._render_empty_state()
            return

        for index, row in enumerate(rows):
            self._render_row(index, row, actions_callback)

    def _render_row(self, index, row, actions_callback):
        bg_color = COLOR_BG_CARD if index % 2 == 0 else "#F8FAFC"

        row_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=bg_color,
            corner_radius=6,
            height=46
        )
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)

        # Row hover effect
        def _on_enter(e):
            row_frame.configure(fg_color="#EEF2F6")

        def _on_leave(e):
            row_frame.configure(fg_color=bg_color)

        row_frame.bind("<Enter>", _on_enter)
        row_frame.bind("<Leave>", _on_leave)

        # Convert row tuple or dict
        row_dict = row if isinstance(row, dict) else {self.columns[i][0]: row[i] for i in range(min(len(row), len(self.columns)))}

        for col_key, col_title, width in self.columns:
            val = row_dict.get(col_key, "")

            if col_key == "status":
                cell_widget = self._create_status_badge(row_frame, str(val), width)
            elif col_key == "actions":
                cell_widget = self._create_action_buttons(row_frame, row_dict, width, actions_callback)
            else:
                cell_widget = ctk.CTkLabel(
                    row_frame,
                    text=str(val),
                    font=FONT_BODY,
                    text_color=COLOR_TEXT_PRIMARY,
                    width=width,
                    anchor="w"
                )
                cell_widget.bind("<Enter>", _on_enter)
                cell_widget.bind("<Leave>", _on_leave)

            cell_widget.pack(side="left", padx=8)

    def _create_status_badge(self, master, status_text, width):
        norm_status = status_text.upper()
        if "ON TIME" in norm_status or "CONFIRMED" in norm_status or "READY" in norm_status:
            bg = "#DCFCE7"
            fg = "#15803D"
        elif "BOARDING" in norm_status or "ACTIVE" in norm_status:
            bg = "#DBEAFE"
            fg = "#1D4ED8"
        elif "DELAYED" in norm_status or "WAITING" in norm_status or "MEDIUM" in norm_status:
            bg = "#FEF3C7"
            fg = "#B45309"
        elif "CANCELLED" in norm_status or "HIGH" in norm_status:
            bg = "#FEE2E2"
            fg = "#B91C1C"
        else:
            bg = "#F1F5F9"
            fg = "#475569"

        container = ctk.CTkFrame(master, fg_color="transparent", width=width)
        container.pack_propagate(False)

        badge = ctk.CTkFrame(container, fg_color=bg, corner_radius=10, height=24)
        badge.pack(side="left")

        lbl = ctk.CTkLabel(
            badge,
            text=f"● {status_text}",
            font=FONT_BADGE,
            text_color=fg,
            padx=10,
            pady=2
        )
        lbl.pack()
        return container

    def _create_action_buttons(self, master, row_data, width, actions_callback):
        container = ctk.CTkFrame(master, fg_color="transparent", width=width)
        container.pack_propagate(False)

        # View button
        btn_view = ctk.CTkButton(
            container,
            text="👁",
            width=28,
            height=26,
            corner_radius=6,
            fg_color="#EFF6FF",
            hover_color="#DBEAFE",
            text_color="#1E40AF",
            font=("Segoe UI", 12),
            command=lambda: actions_callback("view", row_data) if actions_callback else None
        )
        btn_view.pack(side="left", padx=2)

        # Edit button
        btn_edit = ctk.CTkButton(
            container,
            text="✏",
            width=28,
            height=26,
            corner_radius=6,
            fg_color="#F8FAFC",
            hover_color="#E2E8F0",
            text_color="#334155",
            font=("Segoe UI", 12),
            command=lambda: actions_callback("edit", row_data) if actions_callback else None
        )
        btn_edit.pack(side="left", padx=2)

        # Delete button
        btn_delete = ctk.CTkButton(
            container,
            text="🗑",
            width=28,
            height=26,
            corner_radius=6,
            fg_color="#FEF2F2",
            hover_color="#FEE2E2",
            text_color="#DC2626",
            font=("Segoe UI", 12),
            command=lambda: actions_callback("delete", row_data) if actions_callback else None
        )
        btn_delete.pack(side="left", padx=2)

        return container

    def _render_empty_state(self):
        empty_box = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        empty_box.pack(expand=True, pady=40)

        lbl_icon = ctk.CTkLabel(
            empty_box,
            text="✈",
            font=("Segoe UI", 36),
            text_color="#94A3B8"
        )
        lbl_icon.pack(pady=(0, 6))

        lbl_title = ctk.CTkLabel(
            empty_box,
            text=self.empty_title,
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        )
        lbl_title.pack()

        lbl_sub = ctk.CTkLabel(
            empty_box,
            text=self.empty_subtitle,
            font=FONT_BODY,
            text_color=COLOR_TEXT_MUTED
        )
        lbl_sub.pack(pady=(4, 12))

        if self.empty_action_text and self.on_empty_action:
            btn_action = ctk.CTkButton(
                empty_box,
                text=self.empty_action_text,
                fg_color=COLOR_SECONDARY_BLUE,
                hover_color="#1D4ED8",
                corner_radius=8,
                command=self.on_empty_action
            )
            btn_action.pack()
