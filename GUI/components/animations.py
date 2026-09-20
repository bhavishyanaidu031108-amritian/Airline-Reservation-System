"""
Lightweight animation and visual helper routines for SkyLink GUI.
Provides number tweening, canvas aircraft drawing, and route animation utilities.
"""

import math
import tkinter as tk


def animate_counter(label_widget, start_val, end_val, duration_ms=600, prefix="", suffix="", is_currency=False):
    """
    Smoothly animates a numeric value inside a label widget over duration_ms.
    """
    steps = 20
    interval = max(10, duration_ms // steps)
    step_val = (end_val - start_val) / float(steps)

    def _update_step(current_step, current_val):
        if not label_widget.winfo_exists():
            return
        if current_step >= steps:
            final_formatted = _format_value(end_val, is_currency)
            label_widget.configure(text=f"{prefix}{final_formatted}{suffix}")
            return

        new_val = current_val + step_val
        formatted = _format_value(new_val, is_currency)
        label_widget.configure(text=f"{prefix}{formatted}{suffix}")
        label_widget.after(interval, lambda: _update_step(current_step + 1, new_val))

    _update_step(0, start_val)


def _format_value(val, is_currency):
    if is_currency:
        if val >= 100000:
            return f"₹{val / 100000:.1f}L"
        elif val >= 1000:
            return f"₹{val / 1000:.1f}k"
        else:
            return f"₹{int(val):,}"
    else:
        if val >= 1000:
            return f"{int(val):,}"
        return f"{int(val)}"


def draw_airplane(canvas, x, y, size=24, angle=0, fill_color="#38BDF8", outline_color="#0B1F3A"):
    """
    Draws a streamlined modern vector airplane centered at (x, y) with rotation angle (degrees).
    Returns list of canvas item IDs so it can be moved or deleted.
    """
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # Base coordinates of a sleek airplane silhouette facing right (angle=0)
    # Fuselage and wings
    points = [
        (1.0, 0.0),       # Nose tip
        (0.4, -0.2),      # Cockpit right
        (-0.2, -0.9),     # Right wing tip
        (-0.4, -0.9),     # Right wing back edge
        (-0.2, -0.2),     # Right wing root
        (-0.7, -0.2),     # Tail boom right
        (-0.9, -0.5),     # Right stabilizer tip
        (-1.0, -0.5),     # Right stabilizer back
        (-0.95, 0.0),     # Tail tip
        (-1.0, 0.5),      # Left stabilizer back
        (-0.9, 0.5),      # Left stabilizer tip
        (-0.7, 0.2),      # Tail boom left
        (-0.2, 0.2),      # Left wing root
        (-0.4, 0.9),      # Left wing back edge
        (-0.2, 0.9),      # Left wing tip
        (0.4, 0.2),       # Cockpit left
    ]

    transformed_points = []
    scale = size / 2.0
    for px, py in points:
        sx = px * scale
        sy = py * scale
        rx = sx * cos_a - sy * sin_a
        ry = sx * sin_a + sy * cos_a
        transformed_points.extend([x + rx, y + ry])

    plane_id = canvas.create_polygon(
        transformed_points,
        fill=fill_color,
        outline=outline_color,
        width=1.5,
        smooth=True,
        tags="animated_plane"
    )
    return [plane_id]
