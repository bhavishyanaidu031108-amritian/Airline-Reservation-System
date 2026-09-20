"""
Elevated statistics cards with hover animation, icon badges,
and smooth number counting animation.
"""

import customtkinter as ctk
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_SECONDARY_BLUE,
    COLOR_PRIMARY_NAVY, COLOR_TEXT_SECONDARY, COLOR_ACCENT_SKY,
    FONT_CARD_TITLE, FONT_CARD_VALUE, FONT_SMALL
)
from GUI.components.animations import animate_counter


class StatCard(ctk.CTkFrame):
    def __init__(self, master, title, target_value, icon="✈", is_currency=False, subtitle="Updated just now", **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1.5,
            border_color=COLOR_BORDER,
            height=130,
            **kwargs
        )
        self.pack_propagate(False)
        self.title = title
        self.target_value = target_value
        self.icon = icon
        self.is_currency = is_currency
        self.subtitle = subtitle

        self._build_ui()
        self._bind_hover_effects()

    def _build_ui(self):
        # Top Row: Title + Icon Badge
        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(14, 4))

        # Title
        lbl_title = ctk.CTkLabel(
            top_row,
            text=self.title.upper(),
            font=FONT_CARD_TITLE,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        lbl_title.pack(side="left")

        # Icon pill
        icon_badge = ctk.CTkFrame(
            top_row,
            fg_color="#EFF6FF",
            width=36,
            height=36,
            corner_radius=10
        )
        icon_badge.pack(side="right")
        icon_badge.pack_propagate(False)

        lbl_icon = ctk.CTkLabel(
            icon_badge,
            text=self.icon,
            font=("Segoe UI", 16),
            text_color=COLOR_SECONDARY_BLUE
        )
        lbl_icon.place(relx=0.5, rely=0.5, anchor="center")

        # Middle: Animated Value
        self.lbl_value = ctk.CTkLabel(
            self,
            text="₹0" if self.is_currency else "0",
            font=FONT_CARD_VALUE,
            text_color=COLOR_PRIMARY_NAVY,
            anchor="w"
        )
        self.lbl_value.pack(anchor="w", padx=16, pady=(0, 2))

        # Bottom Subtitle / trend indicator
        lbl_sub = ctk.CTkLabel(
            self,
            text=f"● {self.subtitle}",
            font=FONT_SMALL,
            text_color="#10B981",
            anchor="w"
        )
        lbl_sub.pack(anchor="w", padx=16, pady=(0, 10))

        # Trigger animation
        self.after(80, self._start_animation)

    def _start_animation(self):
        animate_counter(
            self.lbl_value,
            start_val=0,
            end_val=self.target_value,
            duration_ms=500,
            is_currency=self.is_currency
        )

    def _bind_hover_effects(self):
        def _on_enter(e):
            self.configure(border_color=COLOR_SECONDARY_BLUE, fg_color="#F8FAFC")

        def _on_leave(e):
            self.configure(border_color=COLOR_BORDER, fg_color=COLOR_BG_CARD)

        self.bind("<Enter>", _on_enter)
        self.bind("<Leave>", _on_leave)
        for child in self.winfo_children():
            child.bind("<Enter>", _on_enter)
            child.bind("<Leave>", _on_leave)

    def update_value(self, new_val):
        self.target_value = new_val
        self._start_animation()
