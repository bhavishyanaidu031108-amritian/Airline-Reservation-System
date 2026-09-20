"""
Interactive Airport Network and Dijkstra Shortest Path Visualization.
Features custom Tkinter Canvas with geographical airport node layout,
animated shortest path trajectory, vector aircraft travel simulation,
and direct connection to RouteService and Dijkstra algorithm.
"""

import math
import customtkinter as ctk
import tkinter as tk
from services.route_service import RouteService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_ACCENT_SKY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_WHITE,
    FONT_HERO, FONT_TITLE, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL,
    FONT_BADGE
)
from GUI.components.animations import draw_airplane


class RouteView(ctk.CTkFrame):
    # Geographically-inspired coordinate layout on 860x420 canvas
    AIRPORT_COORDS = {
        "Mumbai": (190, 130, "BOM"),
        "Hyderabad": (470, 110, "HYD"),
        "Bangalore": (370, 310, "BLR"),
        "Chennai": (670, 270, "MAA"),
    }

    def __init__(self, master, user_info=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.route_service = RouteService()

        self.highlighted_path = []
        self.highlighted_distance = 0
        self._animating = False

        self._build_ui()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=4, pady=4)

        # ----------------------------------------------------
        # TOP SELECTION & QUERY CONTROLS
        # ----------------------------------------------------
        ctrl_card = ctk.CTkFrame(
            scroll,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER
        )
        ctrl_card.pack(fill="x", pady=(0, 16))

        c_inner = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        c_inner.pack(fill="x", padx=24, pady=18)

        # Title
        t_row = ctk.CTkFrame(c_inner, fg_color="transparent")
        t_row.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            t_row,
            text="🗺  Airport Network & Dijkstra Shortest Path",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(side="left")

        ctk.CTkLabel(
            t_row,
            text="Graph Theory + Dijkstra Greedy Algorithm",
            font=FONT_SMALL,
            text_color="#10B981"
        ).pack(side="right")

        # Inputs Row
        row = ctk.CTkFrame(c_inner, fg_color="transparent")
        row.pack(fill="x")

        airports = self.route_service.get_airports()

        # Origin
        o_box = ctk.CTkFrame(row, fg_color="transparent")
        o_box.pack(side="left", padx=(0, 10))
        ctk.CTkLabel(o_box, text="SOURCE AIRPORT", font=FONT_BADGE, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.combo_src = ctk.CTkComboBox(
            o_box,
            values=airports,
            height=38,
            width=180,
            corner_radius=8,
            font=FONT_BODY
        )
        self.combo_src.set("Hyderabad")
        self.combo_src.pack(pady=(2, 0))

        # Destination
        d_box = ctk.CTkFrame(row, fg_color="transparent")
        d_box.pack(side="left", padx=(0, 16))
        ctk.CTkLabel(d_box, text="DESTINATION AIRPORT", font=FONT_BADGE, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w")
        self.combo_dst = ctk.CTkComboBox(
            d_box,
            values=airports,
            height=38,
            width=180,
            corner_radius=8,
            font=FONT_BODY
        )
        self.combo_dst.set("Mumbai")
        self.combo_dst.pack(pady=(2, 0))

        # Find Shortest Route Button
        btn_find = ctk.CTkButton(
            row,
            text="FIND SHORTEST ROUTE  ➔",
            height=38,
            corner_radius=8,
            font=FONT_BODY_BOLD,
            fg_color=COLOR_SECONDARY_BLUE,
            hover_color="#1D4ED8",
            command=self._handle_find_shortest_route
        )
        btn_find.pack(side="left", pady=(16, 0))

        # Preset Quick Button
        btn_preset = ctk.CTkButton(
            row,
            text="Demo: HYD ➔ BOM (1550 km)",
            height=38,
            corner_radius=8,
            font=FONT_SMALL,
            fg_color="#EFF6FF",
            hover_color="#DBEAFE",
            text_color=COLOR_SECONDARY_BLUE,
            command=lambda: self._set_and_run("Hyderabad", "Mumbai")
        )
        btn_preset.pack(side="right", pady=(16, 0))

        # ----------------------------------------------------
        # RESULT SUMMARY CARD
        # ----------------------------------------------------
        self.summary_card = ctk.CTkFrame(
            scroll,
            fg_color="#0A1C36",
            corner_radius=12,
            border_width=1,
            border_color="#1E3A8A"
        )
        self.summary_card.pack(fill="x", pady=(0, 16))

        self.s_inner = ctk.CTkFrame(self.summary_card, fg_color="transparent")
        self.s_inner.pack(fill="x", padx=20, pady=14)

        self.lbl_path_sequence = ctk.CTkLabel(
            self.s_inner,
            text="Select Source & Destination airports to calculate shortest route.",
            font=FONT_SECTION,
            text_color=COLOR_TEXT_WHITE
        )
        self.lbl_path_sequence.pack(side="left")

        self.lbl_total_distance = ctk.CTkLabel(
            self.s_inner,
            text="Total Distance: -- km",
            font=FONT_HERO,
            text_color=COLOR_ACCENT_SKY
        )
        self.lbl_total_distance.pack(side="right")

        # ----------------------------------------------------
        # AIRPORT NETWORK INTERACTIVE CANVAS
        # ----------------------------------------------------
        canvas_wrapper = ctk.CTkFrame(
            scroll,
            fg_color="#07152B",
            corner_radius=14,
            border_width=1.5,
            border_color="#1E3A5F"
        )
        canvas_wrapper.pack(fill="x", pady=(0, 20))

        self.canvas_w = 860
        self.canvas_h = 420

        self.canvas = tk.Canvas(
            canvas_wrapper,
            width=self.canvas_w,
            height=self.canvas_h,
            bg="#07152B",
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)

        self._draw_network()

        # Run initial default route Hyderabad -> Mumbai
        self.after(200, lambda: self._handle_find_shortest_route())

    def _set_and_run(self, src, dst):
        self.combo_src.set(src)
        self.combo_dst.set(dst)
        self._handle_find_shortest_route()

    def _draw_network(self):
        self.canvas.delete("all")

        # Draw radar grid background lines
        for x in range(50, self.canvas_w, 100):
            self.canvas.create_line(x, 0, x, self.canvas_h, fill="#0D2240", width=1)
        for y in range(50, self.canvas_h, 80):
            self.canvas.create_line(0, y, self.canvas_w, y, fill="#0D2240", width=1)

        # Draw radar concentric circle
        cx, cy = self.canvas_w // 2, self.canvas_h // 2
        for r in [120, 220, 320]:
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#0F284C", width=1, dash=(4, 6))

        # Draw all graph routes (edges)
        routes = self.route_service.get_all_routes()
        # routes: list of (source, destination, distance)

        # Check which edges are in the shortest path
        shortest_edges = set()
        if self.highlighted_path and len(self.highlighted_path) > 1:
            for idx in range(len(self.highlighted_path) - 1):
                shortest_edges.add((self.highlighted_path[idx], self.highlighted_path[idx + 1]))

        for src, dst, dist in routes:
            if src in self.AIRPORT_COORDS and dst in self.AIRPORT_COORDS:
                x1, y1, _ = self.AIRPORT_COORDS[src]
                x2, y2, _ = self.AIRPORT_COORDS[dst]

                is_in_path = (src, dst) in shortest_edges

                if is_in_path:
                    # Glowing thick line for shortest route
                    self.canvas.create_line(x1, y1, x2, y2, fill=COLOR_ACCENT_SKY, width=4)
                    self.canvas.create_line(x1, y1, x2, y2, fill="#FFFFFF", width=1.5)
                else:
                    # Standard edge line
                    self.canvas.create_line(x1, y1, x2, y2, fill="#1E3A5F", width=2, dash=(6, 4))

                # Distance badge at midpoint
                mx = (x1 + x2) // 2
                my = (y1 + y2) // 2
                badge_bg = COLOR_SECONDARY_BLUE if is_in_path else "#0D2240"
                badge_fg = "#FFFFFF" if is_in_path else "#94A3B8"

                self.canvas.create_rectangle(
                    mx - 34, my - 11, mx + 34, my + 11,
                    fill=badge_bg, outline=COLOR_ACCENT_SKY if is_in_path else "#1E3A5F", width=1
                )
                self.canvas.create_text(
                    mx, my,
                    text=f"{dist} km",
                    fill=badge_fg,
                    font=("Segoe UI", 9, "bold")
                )

        # Draw Airport Nodes
        for name, (x, y, code) in self.AIRPORT_COORDS.items():
            is_active_node = name in self.highlighted_path

            # Outer glow
            glow_color = "#38BDF8" if is_active_node else "#1E3A5F"
            self.canvas.create_oval(x - 26, y - 26, x + 26, y + 26, outline=glow_color, width=2)

            # Center circle
            fill_color = COLOR_SECONDARY_BLUE if is_active_node else "#0B1F3A"
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=fill_color, outline="#FFFFFF", width=2)

            # 3-Letter Code
            self.canvas.create_text(
                x, y,
                text=code,
                fill="#FFFFFF",
                font=("Segoe UI", 10, "bold")
            )

            # Full city name banner below
            self.canvas.create_text(
                x, y + 36,
                text=name.upper(),
                fill=COLOR_ACCENT_SKY if is_active_node else "#E2E8F0",
                font=("Segoe UI", 11, "bold")
            )

    def _handle_find_shortest_route(self):
        src = self.combo_src.get()
        dst = self.combo_dst.get()

        if src == dst:
            self.highlighted_path = [src]
            self.highlighted_distance = 0
            self.lbl_path_sequence.configure(text=f"Origin and Destination are identical: {src}")
            self.lbl_total_distance.configure(text="Total Distance: 0 km")
            self._draw_network()
            return

        # CALL EXISTING DIJKSTRA VIA RouteService!
        path, total_dist = self.route_service.find_shortest_path(src, dst)

        if not path or total_dist == float('inf'):
            self.highlighted_path = []
            self.highlighted_distance = 0
            self.lbl_path_sequence.configure(text=f"No connected route found between {src} and {dst}.")
            self.lbl_total_distance.configure(text="Unreachable")
            self._draw_network()
            return

        self.highlighted_path = path
        self.highlighted_distance = total_dist

        # Format sequence e.g. HYDERABAD ➔ BANGALORE ➔ MUMBAI
        seq_text = "  ➔  ".join([p.upper() for p in path])
        self.lbl_path_sequence.configure(text=f"Shortest Path: {seq_text}")
        self.lbl_total_distance.configure(text=f"Total Distance: {int(total_dist)} km")

        self._draw_network()
        self._animate_flight_along_path(path)

    def _animate_flight_along_path(self, path):
        if len(path) < 2:
            return

        # Animate aircraft flying along path nodes
        legs = []
        for i in range(len(path) - 1):
            s_node, d_node = path[i], path[i + 1]
            if s_node in self.AIRPORT_COORDS and d_node in self.AIRPORT_COORDS:
                x1, y1, _ = self.AIRPORT_COORDS[s_node]
                x2, y2, _ = self.AIRPORT_COORDS[d_node]
                legs.append((x1, y1, x2, y2))

        if not legs:
            return

        def _run_leg(leg_idx):
            if leg_idx >= len(legs):
                return
            x1, y1, x2, y2 = legs[leg_idx]
            steps = 25
            dx = (x2 - x1) / steps
            dy = (y2 - y1) / steps
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

            def _step(step_idx, cur_x, cur_y):
                if not self.winfo_exists():
                    return
                self.canvas.delete("animated_plane")
                draw_airplane(
                    self.canvas,
                    cur_x, cur_y,
                    size=24,
                    angle=angle,
                    fill_color="#38BDF8",
                    outline_color="#FFFFFF"
                )

                if step_idx < steps:
                    self.after(16, lambda: _step(step_idx + 1, cur_x + dx, cur_y + dy))
                else:
                    self.after(100, lambda: _run_leg(leg_idx + 1))

            _step(0, x1, y1)

        _run_leg(0)
