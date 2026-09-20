"""
Premium Airline Login Screen for SkyLink Airline Reservation System.
Features split-view aviation hero canvas on the left and modern credential
card on the right, backed by the HashTable authentication service.
"""

import customtkinter as ctk
import tkinter as tk
from services.auth_service import AuthService
from GUI.components.theme import (
    COLOR_PRIMARY_NAVY, COLOR_NAVY_DEEP, COLOR_SECONDARY_BLUE,
    COLOR_ACCENT_SKY, COLOR_BG_LIGHT, COLOR_BG_CARD, COLOR_BORDER,
    COLOR_BORDER_FOCUS, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_TEXT_WHITE, COLOR_STATUS_CANCELLED, FONT_HERO, FONT_TITLE,
    FONT_SECTION, FONT_BODY, FONT_SMALL, FONT_BADGE
)
from GUI.components.animations import draw_airplane


class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, on_login_success=None, **kwargs):
        super().__init__(master, fg_color=COLOR_BG_LIGHT, corner_radius=0, **kwargs)
        self.master = master
        self.on_login_success = on_login_success
        self.auth_service = AuthService()

        self._build_ui()

    def _build_ui(self):
        # Container taking full window
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # ----------------------------------------------------
        # LEFT HERO PANEL (Aviation Atmosphere)
        # ----------------------------------------------------
        hero_panel = ctk.CTkFrame(
            container,
            fg_color=COLOR_PRIMARY_NAVY,
            corner_radius=0,
            width=540
        )
        hero_panel.pack(side="left", fill="both", expand=True)
        hero_panel.pack_propagate(False)

        # Aviation Canvas
        self.hero_canvas = tk.Canvas(
            hero_panel,
            bg=COLOR_PRIMARY_NAVY,
            highlightthickness=0
        )
        self.hero_canvas.pack(fill="both", expand=True)

        self.hero_canvas.bind("<Configure>", self._draw_hero_canvas)

        # Overlay text on hero
        hero_overlay = ctk.CTkFrame(hero_panel, fg_color="transparent")
        hero_overlay.place(relx=0.08, rely=0.08, relwidth=0.84)

        lbl_logo = ctk.CTkLabel(
            hero_overlay,
            text="✈  SKYLINK",
            font=("Segoe UI Semibold", 24, "bold"),
            text_color=COLOR_ACCENT_SKY,
            anchor="w"
        )
        lbl_logo.pack(anchor="w")

        lbl_hero_title = ctk.CTkLabel(
            hero_overlay,
            text="Next-Gen Airline\nReservation & Route\nOptimization System",
            font=("Segoe UI", 26, "bold"),
            text_color=COLOR_TEXT_WHITE,
            justify="left",
            anchor="w"
        )
        lbl_hero_title.pack(anchor="w", pady=(18, 12))

        lbl_hero_desc = ctk.CTkLabel(
            hero_overlay,
            text="Integrated with AVL Trees, Dijkstra Shortest Path,\nPriority Queue Waiting Lists & Enterprise SQLite DB.",
            font=FONT_BODY,
            text_color="#94A3B8",
            justify="left",
            anchor="w"
        )
        lbl_hero_desc.pack(anchor="w")

        # Bottom stats preview in hero
        stats_box = ctk.CTkFrame(hero_panel, fg_color="#102544", corner_radius=12, height=76)
        stats_box.place(relx=0.08, rely=0.80, relwidth=0.84)


        s1 = ctk.CTkFrame(stats_box, fg_color="transparent")
        s1.pack(side="left", expand=True)
        ctk.CTkLabel(s1, text="99.9%", font=FONT_SECTION, text_color=COLOR_ACCENT_SKY).pack()
        ctk.CTkLabel(s1, text="Flight Uptime", font=FONT_SMALL, text_color="#94A3B8").pack()

        s2 = ctk.CTkFrame(stats_box, fg_color="transparent")
        s2.pack(side="left", expand=True)
        ctk.CTkLabel(s2, text="O(log n)", font=FONT_SECTION, text_color=COLOR_ACCENT_SKY).pack()
        ctk.CTkLabel(s2, text="AVL Efficiency", font=FONT_SMALL, text_color="#94A3B8").pack()

        s3 = ctk.CTkFrame(stats_box, fg_color="transparent")
        s3.pack(side="left", expand=True)
        ctk.CTkLabel(s3, text="Dijkstra", font=FONT_SECTION, text_color=COLOR_ACCENT_SKY).pack()
        ctk.CTkLabel(s3, text="Shortest Route", font=FONT_SMALL, text_color="#94A3B8").pack()

        # ----------------------------------------------------
        # RIGHT LOGIN FORM PANEL
        # ----------------------------------------------------
        right_panel = ctk.CTkFrame(
            container,
            fg_color=COLOR_BG_LIGHT,
            corner_radius=0
        )
        right_panel.pack(side="right", fill="both", expand=True)

        # Centered Login Card
        card = ctk.CTkFrame(
            right_panel,
            fg_color=COLOR_BG_CARD,
            corner_radius=16,
            border_width=1.5,
            border_color=COLOR_BORDER,
            width=420
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Form content
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(padx=36, pady=36, fill="both")

        lbl_welcome = ctk.CTkLabel(
            form,
            text="Welcome Back",
            font=FONT_HERO,
            text_color=COLOR_PRIMARY_NAVY,
            anchor="w"
        )
        lbl_welcome.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(
            form,
            text="Sign in to your SkyLink portal account.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            anchor="w"
        )
        lbl_sub.pack(anchor="w", pady=(4, 20))

        # Role Selector Pill
        role_frame = ctk.CTkFrame(form, fg_color="#F1F5F9", corner_radius=8, height=36)
        role_frame.pack(fill="x", pady=(0, 18))
        role_frame.pack_propagate(False)

        self.selected_role = tk.StringVar(value="Admin")

        self.btn_role_admin = ctk.CTkButton(
            role_frame,
            text="Administrator",
            corner_radius=6,
            height=28,
            font=FONT_SMALL,
            fg_color=COLOR_SECONDARY_BLUE,
            text_color=COLOR_TEXT_WHITE,
            command=lambda: self._select_role("Admin")
        )
        self.btn_role_admin.pack(side="left", expand=True, fill="both", padx=3, pady=3)

        self.btn_role_passenger = ctk.CTkButton(
            role_frame,
            text="Passenger",
            corner_radius=6,
            height=28,
            font=FONT_SMALL,
            fg_color="transparent",
            text_color=COLOR_TEXT_SECONDARY,
            hover_color="#E2E8F0",
            command=lambda: self._select_role("Passenger")
        )
        self.btn_role_passenger.pack(side="left", expand=True, fill="both", padx=3, pady=3)

        # Username Input
        lbl_u = ctk.CTkLabel(form, text="Username / Passenger ID", font=FONT_SMALL, text_color=COLOR_TEXT_PRIMARY, anchor="w")
        lbl_u.pack(anchor="w")

        self.entry_username = ctk.CTkEntry(
            form,
            placeholder_text="e.g. admin or bhavishya",
            height=40,
            corner_radius=8,
            border_color=COLOR_BORDER,
            font=FONT_BODY
        )
        self.entry_username.pack(fill="x", pady=(4, 14))
        self.entry_username.insert(0, "admin")

        # Password Input
        lbl_p = ctk.CTkLabel(form, text="Password", font=FONT_SMALL, text_color=COLOR_TEXT_PRIMARY, anchor="w")
        lbl_p.pack(anchor="w")

        p_row = ctk.CTkFrame(form, fg_color="transparent")
        p_row.pack(fill="x", pady=(4, 8))

        self.entry_password = ctk.CTkEntry(
            p_row,
            placeholder_text="Enter password",
            show="*",
            height=40,
            corner_radius=8,
            border_color=COLOR_BORDER,
            font=FONT_BODY
        )
        self.entry_password.pack(side="left", fill="x", expand=True)
        self.entry_password.insert(0, "admin123")

        self.btn_toggle_eye = ctk.CTkButton(
            p_row,
            text="👁",
            width=38,
            height=40,
            corner_radius=8,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color=COLOR_TEXT_SECONDARY,
            command=self._toggle_password_visibility
        )
        self.btn_toggle_eye.pack(side="left", padx=(6, 0))

        # Error notification banner
        self.lbl_error = ctk.CTkLabel(
            form,
            text="",
            font=FONT_SMALL,
            text_color=COLOR_STATUS_CANCELLED,
            wraplength=340,
            justify="left"
        )
        self.lbl_error.pack(anchor="w", pady=(0, 10))

        # Sign In Button
        self.btn_login = ctk.CTkButton(
            form,
            text="Sign In to SkyLink  ➔",
            height=44,
            corner_radius=8,
            font=FONT_SECTION,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._handle_login
        )
        self.btn_login.pack(fill="x", pady=(4, 16))

        # Quick Demo Credential Pills
        demo_box = ctk.CTkFrame(form, fg_color="#F8FAFC", corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        demo_box.pack(fill="x")

        lbl_demo = ctk.CTkLabel(
            demo_box,
            text="Demo Credentials (Click to fill):",
            font=("Segoe UI", 10, "bold"),
            text_color=COLOR_TEXT_SECONDARY
        )
        lbl_demo.pack(anchor="w", padx=10, pady=(6, 2))

        chips_row = ctk.CTkFrame(demo_box, fg_color="transparent")
        chips_row.pack(fill="x", padx=8, pady=(0, 6))

        btn_fill_admin = ctk.CTkButton(
            chips_row,
            text="Admin (admin / admin123)",
            height=24,
            font=("Segoe UI", 10),
            corner_radius=4,
            fg_color="#EFF6FF",
            text_color=COLOR_SECONDARY_BLUE,
            hover_color="#DBEAFE",
            command=lambda: self._quick_fill("admin", "admin123", "Admin")
        )
        btn_fill_admin.pack(side="left", padx=2)

        btn_fill_pass = ctk.CTkButton(
            chips_row,
            text="Passenger (bhavishya / pass123)",
            height=24,
            font=("Segoe UI", 10),
            corner_radius=4,
            fg_color="#F0FDF4",
            text_color="#15803D",
            hover_color="#DCFCE7",
            command=lambda: self._quick_fill("bhavishya", "pass123", "Passenger")
        )
        btn_fill_pass.pack(side="left", padx=2)

        # Enter key triggers login
        self.entry_password.bind("<Return>", lambda e: self._handle_login())
        self.entry_username.bind("<Return>", lambda e: self._handle_login())

    def _draw_hero_canvas(self, event=None):
        w = self.hero_canvas.winfo_width()
        h = self.hero_canvas.winfo_height()
        if w < 50 or h < 50:
            return

        self.hero_canvas.delete("all")

        # Subtle radar concentric circles in top right
        cx, cy = int(w * 0.85), int(h * 0.35)
        for r in [60, 120, 180, 240]:
            self.hero_canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline="#122B4D", width=1, dash=(3, 5)
            )

        # Radar sweep ray
        self.hero_canvas.create_line(
            cx, cy, cx - 170, cy + 170,
            fill="#1A3B66", width=1.5
        )

        # Runway perspective lines at bottom
        rx, ry = int(w * 0.5), h
        self.hero_canvas.create_line(rx - 80, ry, rx - 30, int(h * 0.65), fill="#1A3A62", width=1.5)
        self.hero_canvas.create_line(rx + 80, ry, rx + 30, int(h * 0.65), fill="#1A3A62", width=1.5)
        self.hero_canvas.create_line(rx, ry, rx, int(h * 0.65), fill="#2563EB", width=2, dash=(10, 8))

        # Vector aircraft climbing into sky
        draw_airplane(
            self.hero_canvas,
            x=int(w * 0.5),
            y=int(h * 0.52),
            size=64,
            angle=-25,
            fill_color=COLOR_ACCENT_SKY,
            outline_color=COLOR_TEXT_WHITE
        )

        # Flight trail dots
        for i in range(1, 6):
            tx = int(w * 0.5) - (i * 24)
            ty = int(h * 0.52) + (i * 12)
            self.hero_canvas.create_oval(
                tx - 3, ty - 3, tx + 3, ty + 3,
                fill=COLOR_SECONDARY_BLUE, outline=COLOR_ACCENT_SKY
            )

    def _select_role(self, role):
        self.selected_role.set(role)
        if role == "Admin":
            self.btn_role_admin.configure(fg_color=COLOR_SECONDARY_BLUE, text_color=COLOR_TEXT_WHITE)
            self.btn_role_passenger.configure(fg_color="transparent", text_color=COLOR_TEXT_SECONDARY)
        else:
            self.btn_role_passenger.configure(fg_color=COLOR_SECONDARY_BLUE, text_color=COLOR_TEXT_WHITE)
            self.btn_role_admin.configure(fg_color="transparent", text_color=COLOR_TEXT_SECONDARY)

    def _quick_fill(self, username, password, role):
        self._select_role(role)
        self.entry_username.delete(0, "end")
        self.entry_username.insert(0, username)
        self.entry_password.delete(0, "end")
        self.entry_password.insert(0, password)
        self.lbl_error.configure(text="")

    def _toggle_password_visibility(self):
        current_show = self.entry_password.cget("show")
        if current_show == "*":
            self.entry_password.configure(show="")
            self.btn_toggle_eye.configure(text="🔒")
        else:
            self.entry_password.configure(show="*")
            self.btn_toggle_eye.configure(text="👁")

    def _handle_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            self.lbl_error.configure(text="Please enter both username and password.")
            return

        role = self.auth_service.authenticate(username, password)

        if role is not None:
            self.lbl_error.configure(text="")
            if self.on_login_success:
                user_info = {
                    "username": username,
                    "role": role
                }
                self.on_login_success(user_info)
        else:
            self.lbl_error.configure(
                text="Invalid credentials. Please verify your username and password."
            )
