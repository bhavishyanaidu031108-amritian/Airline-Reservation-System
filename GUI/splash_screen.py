"""
Aviation Splash Screen for SkyLink Airline Reservation System.
Shows an animated aircraft traversing the flight trajectory
with real-time connection status transitions.
"""

import math
import customtkinter as ctk
import tkinter as tk
from GUI.components.theme import (
    COLOR_PRIMARY_NAVY, COLOR_NAVY_DEEP, COLOR_ACCENT_SKY,
    COLOR_SECONDARY_BLUE, COLOR_TEXT_WHITE, COLOR_TEXT_MUTED
)
from GUI.components.animations import draw_airplane


class SplashScreen(ctk.CTkToplevel):
    def __init__(self, on_finish=None):
        super().__init__()
        self.on_finish = on_finish
        self.width = 640
        self.height = 380

        self.overrideredirect(True)
        self.configure(fg_color=COLOR_NAVY_DEEP)

        self._center_window()
        self._build_ui()
        self._start_animation()

    def _center_window(self):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - self.width) // 2
        y = (screen_h - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def _build_ui(self):
        main_container = ctk.CTkFrame(self, fg_color=COLOR_NAVY_DEEP, corner_radius=0)
        main_container.pack(fill="both", expand=True)

        # Airline Logo & Title
        lbl_logo = ctk.CTkLabel(
            main_container,
            text="✈",
            font=("Segoe UI", 48, "bold"),
            text_color=COLOR_ACCENT_SKY
        )
        lbl_logo.pack(pady=(40, 4))

        lbl_brand = ctk.CTkLabel(
            main_container,
            text="SKYLINK",
            font=("Segoe UI Semibold", 28, "bold"),
            text_color=COLOR_TEXT_WHITE
        )
        lbl_brand.pack()

        lbl_sub = ctk.CTkLabel(
            main_container,
            text="AIRLINE RESERVATION SYSTEM",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_ACCENT_SKY
        )
        lbl_sub.pack(pady=(2, 24))

        # Canvas for airplane animation trajectory
        self.canvas_w = 520
        self.canvas_h = 70
        self.canvas = tk.Canvas(
            main_container,
            width=self.canvas_w,
            height=self.canvas_h,
            bg=COLOR_NAVY_DEEP,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Base trajectory line with glow
        self.line_y = 35
        self.start_x = 40
        self.end_x = self.canvas_w - 40

        # Dashed background flight path
        self.canvas.create_line(
            self.start_x, self.line_y,
            self.end_x, self.line_y,
            fill="#1E3A5F",
            width=2,
            dash=(6, 4)
        )

        # Status Label
        self.lbl_status = ctk.CTkLabel(
            main_container,
            text="Connecting to Flight Network...",
            font=("Segoe UI", 13, "normal"),
            text_color="#94A3B8"
        )
        self.lbl_status.pack(pady=(12, 0))

        # Version tag
        lbl_ver = ctk.CTkLabel(
            main_container,
            text="v2.4 Enterprise Edition • BTech Project",
            font=("Segoe UI", 10),
            text_color="#475569"
        )
        lbl_ver.pack(side="bottom", pady=12)

    def _start_animation(self):
        total_duration = 2300  # ms
        steps = 60
        interval = total_duration // steps
        distance = self.end_x - self.start_x
        step_dist = distance / steps

        self.current_x = self.start_x
        self.current_step = 0

        # Draw start airport node
        self.canvas.create_oval(
            self.start_x - 5, self.line_y - 5,
            self.start_x + 5, self.line_y + 5,
            fill=COLOR_SECONDARY_BLUE, outline=COLOR_ACCENT_SKY, width=1.5
        )
        # Draw destination airport node
        self.canvas.create_oval(
            self.end_x - 5, self.line_y - 5,
            self.end_x + 5, self.line_y + 5,
            fill="#1E3A5F", outline=COLOR_ACCENT_SKY, width=1.5
        )

        self._active_path_line = self.canvas.create_line(
            self.start_x, self.line_y,
            self.start_x, self.line_y,
            fill=COLOR_ACCENT_SKY,
            width=2.5
        )

        def _step():
            if not self.winfo_exists():
                return
            if self.current_step >= steps:
                self.lbl_status.configure(text="System Ready  ✓", text_color="#10B981")
                self.after(350, self._finish)
                return

            self.current_x += step_dist
            self.current_step += 1

            # Update illuminated line
            self.canvas.coords(
                self._active_path_line,
                self.start_x, self.line_y,
                self.current_x, self.line_y
            )

            # Redraw animated airplane
            self.canvas.delete("animated_plane")
            draw_airplane(
                self.canvas,
                self.current_x, self.line_y,
                size=22,
                angle=0,
                fill_color=COLOR_ACCENT_SKY,
                outline_color=COLOR_TEXT_WHITE
            )

            if self.current_step == int(steps * 0.65):
                self.lbl_status.configure(text="Loading Airway Graphs & AVL Trees...")
            elif self.current_step == int(steps * 0.85):
                self.lbl_status.configure(text="Initializing SkyLink Interface...")

            self.after(interval, _step)

        _step()

    def _finish(self):
        self.destroy()
        if self.on_finish:
            self.on_finish()
