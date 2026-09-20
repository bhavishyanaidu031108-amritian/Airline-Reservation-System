"""
Revenue Analysis View for SkyLink Airline Reservation System.
Embeds Matplotlib charts (Revenue by Flight Bar Chart, Booking Status Donut Chart)
and provides detailed revenue breakdown tables backed by RevenueService and SQLite.
"""

import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from services.revenue_service import RevenueService
from GUI.components.theme import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_PRIMARY_NAVY, COLOR_SECONDARY_BLUE,
    COLOR_ACCENT_SKY, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, FONT_HERO,
    FONT_TITLE, FONT_SECTION, FONT_BODY, FONT_BODY_BOLD, FONT_SMALL
)
from GUI.components.cards import StatCard
from GUI.components.tables import ModernTable


class RevenueView(ctk.CTkFrame):
    def __init__(self, master, user_info=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.user_info = user_info or {"username": "Admin", "role": "Admin"}
        self.revenue_service = RevenueService()

        self._build_ui()
        self.load_analytics()

    def _build_ui(self):
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=4, pady=4)

        # ----------------------------------------------------
        # TOP HEADER
        # ----------------------------------------------------
        top_bar = ctk.CTkFrame(self.scroll, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            top_bar,
            text="📊  Revenue Analytics & Commercial Dashboard",
            font=FONT_TITLE,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(side="left")

        # ----------------------------------------------------
        # KPI METRIC CARDS
        # ----------------------------------------------------
        cards_grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        cards_grid.pack(fill="x", pady=(0, 20))
        cards_grid.columnconfigure((0, 1, 2, 3), weight=1, uniform="rev_cards")

        analytics = self.revenue_service.get_revenue_analytics()

        self.card_total = StatCard(
            cards_grid,
            title="Total Revenue",
            target_value=analytics["total_revenue"],
            icon="₹",
            is_currency=True,
            subtitle="Gross Ticket Receipts"
        )
        self.card_total.grid(row=0, column=0, padx=6, pady=4, sticky="nsew")

        self.card_confirmed = StatCard(
            cards_grid,
            title="Confirmed Bookings",
            target_value=analytics["confirmed_count"],
            icon="✓",
            subtitle="Active Revenue Seats"
        )
        self.card_confirmed.grid(row=0, column=1, padx=6, pady=4, sticky="nsew")

        self.card_cancelled = StatCard(
            cards_grid,
            title="Cancelled Bookings",
            target_value=analytics["cancelled_count"],
            icon="❌",
            subtitle="Refunded Reservations"
        )
        self.card_cancelled.grid(row=0, column=2, padx=6, pady=4, sticky="nsew")

        self.card_avg = StatCard(
            cards_grid,
            title="Average Ticket Fare",
            target_value=analytics["avg_fare"],
            icon="₹",
            is_currency=True,
            subtitle="Yield Per Confirmed Seat"
        )
        self.card_avg.grid(row=0, column=3, padx=6, pady=4, sticky="nsew")

        # ----------------------------------------------------
        # CHARTS ROW (BAR CHART + DONUT CHART)
        # ----------------------------------------------------
        charts_row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        charts_row.pack(fill="x", pady=(0, 20))
        charts_row.columnconfigure((0, 1), weight=1, uniform="charts")

        # 1. Bar Chart Container: Revenue by Flight
        self.bar_card = ctk.CTkFrame(
            charts_row,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER,
            height=320
        )
        self.bar_card.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        self.bar_card.pack_propagate(False)

        # 2. Donut Chart Container: Booking Status
        self.donut_card = ctk.CTkFrame(
            charts_row,
            fg_color=COLOR_BG_CARD,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_BORDER,
            height=320
        )
        self.donut_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        self.donut_card.pack_propagate(False)

        # ----------------------------------------------------
        # DETAILED REVENUE TABLE
        # ----------------------------------------------------
        ctk.CTkLabel(
            self.scroll,
            text="📑  Flight Route Commercial Breakdown",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(anchor="w", pady=(8, 8))

        columns = [
            ("flight_no", "Flight No", 100),
            ("route", "Route (Origin ➔ Destination)", 240),
            ("confirmed", "Confirmed Seats", 140),
            ("revenue", "Generated Revenue", 140),
            ("status", "Route Commercial Status", 150)
        ]

        self.table = ModernTable(
            self.scroll,
            columns=columns,
            empty_title="No Revenue Data",
            empty_subtitle="Bookings will generate financial metrics.",
            height=200
        )
        self.table.pack(fill="both", expand=True)

    def load_analytics(self):
        analytics = self.revenue_service.get_revenue_analytics()
        flight_revenues = analytics["flight_revenues"]

        # Render Bar Chart
        self._render_bar_chart(flight_revenues)

        # Render Donut Chart
        self._render_donut_chart(analytics["confirmed_count"], analytics["cancelled_count"])

        # Render Table
        rows = []
        for fr in flight_revenues:
            fn, src, dst, conf_seats, rev = fr
            rows.append({
                "flight_no": f"SK-{fn}",
                "route": f"{src} ➔ {dst}",
                "confirmed": f"{conf_seats} Bookings",
                "revenue": f"₹{rev:,.2f}",
                "status": "PROFITABLE" if rev > 0 else "NO SALES"
            })
        self.table.set_data(rows)

    def _render_bar_chart(self, flight_revenues):
        for child in self.bar_card.winfo_children():
            child.destroy()

        ctk.CTkLabel(
            self.bar_card,
            text="Revenue by Scheduled Flight",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(anchor="w", padx=16, pady=(12, 4))

        labels = [f"SK-{fr[0]}\n{fr[1][:3]}→{fr[2][:3]}" for fr in flight_revenues] if flight_revenues else ["No Data"]
        values = [fr[4] for fr in flight_revenues] if flight_revenues else [0]

        fig = Figure(figsize=(4.2, 2.4), dpi=90, facecolor="#FFFFFF")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#FFFFFF")

        bars = ax.bar(labels, values, color="#2563EB", width=0.45, edgecolor="#1D4ED8", linewidth=1.2)

        # Style axes
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#E2E8F0")
        ax.spines["bottom"].set_color("#E2E8F0")
        ax.tick_params(axis="both", colors="#64748B", labelsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.5, color="#E2E8F0")

        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.annotate(
                    f"₹{int(h):,}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=8,
                    fontweight="bold",
                    color="#0B1F3A"
                )

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.bar_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _render_donut_chart(self, confirmed_count, cancelled_count):
        for child in self.donut_card.winfo_children():
            child.destroy()

        ctk.CTkLabel(
            self.donut_card,
            text="Booking Status Distribution",
            font=FONT_SECTION,
            text_color=COLOR_PRIMARY_NAVY
        ).pack(anchor="w", padx=16, pady=(12, 4))

        fig = Figure(figsize=(4.2, 2.4), dpi=90, facecolor="#FFFFFF")
        ax = fig.add_subplot(111)

        total = confirmed_count + cancelled_count
        if total == 0:
            sizes = [1]
            colors = ["#E2E8F0"]
            labels = ["No Data"]
        else:
            sizes = [confirmed_count, cancelled_count]
            colors = ["#10B981", "#EF4444"]
            labels = [f"Confirmed ({confirmed_count})", f"Cancelled ({cancelled_count})"]

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.0f%%" if total > 0 else "",
            startangle=90,
            pctdistance=0.75,
            textprops={"fontsize": 8, "color": "#0B1F3A"}
        )

        for at in autotexts:
            at.set_color("#FFFFFF")
            at.set_fontweight("bold")

        # Donut center circle
        centre_circle = matplotlib.patches.Circle((0, 0), 0.55, fc="#FFFFFF")
        fig.gca().add_artist(centre_circle)

        ax.axis("equal")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.donut_card)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(0, 8))
