"""
Sidebar navigation component with smooth expand/collapse animation,
aviation-themed iconography, and role-based menu filtering.
"""

import customtkinter as ctk
from GUI.components.theme import (
    COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE, COLOR_ACCENT_SKY,
    COLOR_TEXT_WHITE, COLOR_TEXT_MUTED, FONT_SECTION, FONT_NAV,
    FONT_NAV_ACTIVE, FONT_SMALL
)


class Sidebar(ctk.CTkFrame):
    EXPANDED_WIDTH = 230
    COLLAPSED_WIDTH = 68

    def __init__(self, master, current_view="dashboard", on_navigate=None, role="Admin", on_logout=None, **kwargs):
        super().__init__(
            master,
            fg_color=COLOR_PRIMARY_NAVY,
            corner_radius=0,
            width=self.EXPANDED_WIDTH,
            **kwargs
        )
        self.pack_propagate(False)
        self.current_view = current_view
        self.on_navigate = on_navigate
        self.role = role
        self.on_logout = on_logout
        self.is_expanded = True
        self.current_width = self.EXPANDED_WIDTH
        self._animating = False

        self.buttons = {}

        self._build_ui()

    def _get_menu_items(self):
        items = [
            ("dashboard", "✈", "Dashboard"),
            ("flights", "🛫", "Flights"),
            ("passengers", "👤", "Passengers"),
            ("bookings", "🎫", "Bookings"),
            ("cancellation", "❌", "Cancellation"),
            ("waiting_list", "⏳", "Waiting List"),
            ("routes", "🗺", "Routes (Dijkstra)"),
            ("revenue", "📊", "Revenue"),
            ("settings", "⚙", "Settings"),
        ]

        if self.role != "Admin":
            # Filter for passenger role
            allowed = {"dashboard", "flights", "bookings", "cancellation", "routes", "settings"}
            items = [item for item in items if item[0] in allowed]

        return items

    def _build_ui(self):
        # Top Branding Banner
        self.brand_frame = ctk.CTkFrame(self, fg_color="transparent", height=78)
        self.brand_frame.pack(fill="x", padx=12, pady=(12, 10))
        self.brand_frame.pack_propagate(False)

        # Airplane Icon + App Title
        self.lbl_logo_icon = ctk.CTkLabel(
            self.brand_frame,
            text="✈",
            font=("Segoe UI", 22, "bold"),
            text_color=COLOR_ACCENT_SKY,
            width=32
        )
        self.lbl_logo_icon.pack(side="left", padx=(4, 8))

        self.title_container = ctk.CTkFrame(self.brand_frame, fg_color="transparent")
        self.title_container.pack(side="left", fill="both", expand=True)

        self.lbl_brand_name = ctk.CTkLabel(
            self.title_container,
            text="SKYLINK",
            font=FONT_SECTION,
            text_color=COLOR_TEXT_WHITE,
            anchor="w"
        )
        self.lbl_brand_name.pack(anchor="w")

        self.lbl_brand_sub = ctk.CTkLabel(
            self.title_container,
            text="Aviation Systems",
            font=FONT_SMALL,
            text_color=COLOR_ACCENT_SKY,
            anchor="w"
        )
        self.lbl_brand_sub.pack(anchor="w")

        # Toggle Button
        self.btn_toggle = ctk.CTkButton(
            self.brand_frame,
            text="◀",
            width=28,
            height=28,
            corner_radius=6,
            fg_color="#132D52",
            hover_color=COLOR_SECONDARY_BLUE,
            text_color=COLOR_TEXT_WHITE,
            command=self.toggle_collapse
        )
        self.btn_toggle.pack(side="right")

        # Divider
        self.divider = ctk.CTkFrame(self, fg_color="#1E3A5F", height=1)
        self.divider.pack(fill="x", padx=14, pady=(0, 14))

        # Navigation Menu List
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="both", expand=True, padx=8)

        for key, icon, label in self._get_menu_items():
            btn = ctk.CTkButton(
                self.nav_frame,
                text=f"{icon}   {label}" if self.is_expanded else icon,
                height=42,
                corner_radius=8,
                anchor="w" if self.is_expanded else "center",
                font=FONT_NAV,
                fg_color="transparent",
                hover_color="#163761",
                text_color=COLOR_TEXT_WHITE,
                command=lambda k=key: self._on_item_click(k)
            )
            btn.pack(fill="x", pady=3)
            self.buttons[key] = (btn, icon, label)

        # Bottom Logout Button
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", side="bottom", padx=8, pady=(0, 16))

        self.btn_logout = ctk.CTkButton(
            self.bottom_frame,
            text="🚪   Logout" if self.is_expanded else "🚪",
            height=40,
            corner_radius=8,
            anchor="w" if self.is_expanded else "center",
            font=FONT_NAV,
            fg_color="#1F1A24",
            hover_color="#DC2626",
            text_color="#F87171",
            command=self.on_logout
        )
        self.btn_logout.pack(fill="x")

        self.set_active_view(self.current_view)

    def _on_item_click(self, key):
        self.set_active_view(key)
        if self.on_navigate:
            self.on_navigate(key)

    def set_active_view(self, key):
        self.current_view = key
        for k, (btn, icon, label) in self.buttons.items():
            if k == key:
                btn.configure(
                    fg_color=COLOR_SECONDARY_BLUE,
                    text_color=COLOR_TEXT_WHITE,
                    font=FONT_NAV_ACTIVE
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="#CBD5E1",
                    font=FONT_NAV
                )

    def toggle_collapse(self):
        if self._animating:
            return
        self.is_expanded = not self.is_expanded
        target_width = self.EXPANDED_WIDTH if self.is_expanded else self.COLLAPSED_WIDTH
        self._animate_width(target_width)

    def _animate_width(self, target_width):
        self._animating = True
        step = 25 if target_width > self.current_width else -25

        def _step():
            if not self.winfo_exists():
                return
            new_w = self.current_width + step
            if (step > 0 and new_w >= target_width) or (step < 0 and new_w <= target_width):
                new_w = target_width
                self.current_width = new_w
                self.configure(width=new_w)
                self._update_elements_for_state()
                self._animating = False
                return

            self.current_width = new_w
            self.configure(width=new_w)
            self.after(12, _step)

        _step()

    def _update_elements_for_state(self):
        if self.is_expanded:
            self.title_container.pack(side="left", fill="both", expand=True)
            self.btn_toggle.configure(text="◀")
            self.btn_logout.configure(text="🚪   Logout", anchor="w")
            for k, (btn, icon, label) in self.buttons.items():
                btn.configure(text=f"{icon}   {label}", anchor="w")
        else:
            self.title_container.pack_forget()
            self.btn_toggle.configure(text="▶")
            self.btn_logout.configure(text="🚪", anchor="center")
            for k, (btn, icon, label) in self.buttons.items():
                btn.configure(text=icon, anchor="center")
