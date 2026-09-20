"""
Modern Header component with greeting, subtitle, dynamic date/clock,
role badge, user profile avatar, and quick logout.
"""

from datetime import datetime
import customtkinter as ctk
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_BORDER,
    COLOR_ACCENT_SKY, FONT_HERO, FONT_SECTION, FONT_SMALL, FONT_BADGE
)


class Header(ctk.CTkFrame):
    def __init__(self, master, username="Admin", role="Admin", on_logout=None, **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER,
            height=78,
            **kwargs
        )
        self.pack_propagate(False)
        self.username = username
        self.role = role
        self.on_logout = on_logout

        self._build_ui()
        self._update_clock()

    def _get_greeting(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good Morning"
        elif 12 <= hour < 17:
            return "Good Afternoon"
        else:
            return "Good Evening"

    def _build_ui(self):
        # Left side: Greeting and Subtitle
        left_container = ctk.CTkFrame(self, fg_color="transparent")
        left_container.pack(side="left", padx=(20, 10), pady=12, fill="y")

        greeting_text = f"{self._get_greeting()}, {self.username.capitalize()}"
        self.lbl_greeting = ctk.CTkLabel(
            left_container,
            text=greeting_text,
            font=FONT_HERO,
            text_color=COLOR_PRIMARY_NAVY,
            anchor="w"
        )
        self.lbl_greeting.pack(anchor="w")

        self.lbl_subtitle = ctk.CTkLabel(
            left_container,
            text="Here's your flight network overview.",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        self.lbl_subtitle.pack(anchor="w")

        # Right side: Clock, Role Badge, Profile Avatar, Logout
        right_container = ctk.CTkFrame(self, fg_color="transparent")
        right_container.pack(side="right", padx=(10, 20), pady=12, fill="y")

        # Clock & Date
        clock_container = ctk.CTkFrame(right_container, fg_color="transparent")
        clock_container.pack(side="left", padx=(0, 15))

        self.lbl_time = ctk.CTkLabel(
            clock_container,
            text="--:--:--",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY,
            anchor="e"
        )
        self.lbl_time.pack(anchor="e")

        self.lbl_date = ctk.CTkLabel(
            clock_container,
            text=datetime.now().strftime("%a, %d %b %Y"),
            font=FONT_SMALL,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="e"
        )
        self.lbl_date.pack(anchor="e")

        # Role Badge
        badge_color = COLOR_SECONDARY_BLUE if self.role == "Admin" else "#0D9488"
        role_frame = ctk.CTkFrame(
            right_container,
            fg_color=badge_color,
            corner_radius=14,
            height=28
        )
        role_frame.pack(side="left", padx=(0, 15))
        lbl_role = ctk.CTkLabel(
            role_frame,
            text=f"✈  {self.role.upper()}",
            font=FONT_BADGE,
            text_color="#FFFFFF",
            padx=12,
            pady=4
        )
        lbl_role.pack()

        # User Avatar Circle
        initials = (self.username[:2]).upper()
        avatar_frame = ctk.CTkFrame(
            right_container,
            fg_color=COLOR_PRIMARY_NAVY,
            width=38,
            height=38,
            corner_radius=19
        )
        avatar_frame.pack(side="left", padx=(0, 10))
        avatar_frame.pack_propagate(False)

        lbl_initials = ctk.CTkLabel(
            avatar_frame,
            text=initials,
            font=FONT_BADGE,
            text_color=COLOR_ACCENT_SKY
        )
        lbl_initials.place(relx=0.5, rely=0.5, anchor="center")

        # Logout Button
        if self.on_logout:
            btn_logout = ctk.CTkButton(
                right_container,
                text="Logout",
                width=72,
                height=32,
                corner_radius=8,
                fg_color="#FEE2E2",
                hover_color="#FCA5A5",
                text_color="#DC2626",
                font=FONT_SMALL,
                command=self.on_logout
            )
            btn_logout.pack(side="left", padx=(5, 0))

    def _update_clock(self):
        if not self.winfo_exists():
            return
        now = datetime.now()
        self.lbl_time.configure(text=now.strftime("%I:%M:%S %p"))
        self.after(1000, self._update_clock)
