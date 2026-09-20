"""
Passenger Dashboard entrypoint for SkyLink Airline Reservation System.
Provides passenger view controls, flight search, ticket booking wizard,
cancellation, and airport route explorer.
"""

from GUI.main_window import MainWindow


class PassengerDashboard(MainWindow):
    def __init__(self, master, username="bhavishya", on_logout=None, **kwargs):
        super().__init__(
            master,
            user_info={"username": username, "role": "Passenger"},
            on_logout=on_logout,
            **kwargs
        )
