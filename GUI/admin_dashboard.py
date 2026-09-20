"""
Admin Dashboard entrypoint for SkyLink Airline Reservation System.
Provides administrative view controls, flight management, passenger management,
waiting list priority queue, and revenue analytics.
"""

from GUI.main_window import MainWindow


class AdminDashboard(MainWindow):
    def __init__(self, master, username="admin", on_logout=None, **kwargs):
        super().__init__(
            master,
            user_info={"username": username, "role": "Admin"},
            on_logout=on_logout,
            **kwargs
        )
