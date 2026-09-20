"""
Main Entrypoint for the SkyLink Airline Reservation System.
Initializes the SQLite database, launches the animated splash screen,
and transitions smoothly into the login screen and airline management dashboard.
"""

import sys
import os
import customtkinter as ctk

# Ensure workspace root is in python module search path
workspace_dir = os.path.dirname(os.path.abspath(__file__))
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

from DATABASE.schema import create_tables
from GUI.splash_screen import SplashScreen
from GUI.login_window import LoginWindow
from GUI.main_window import MainWindow


class SkyLinkApp:
    def __init__(self):
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Create root window
        self.root = ctk.CTk()
        self.root.title("SkyLink - Airline Reservation & Network Management System")
        self.root.geometry("1366x768")
        self.root.minsize(1024, 600)

        # Center root window on display
        self._center_window(1366, 768)

        # Ensure database tables exist
        create_tables()

        # Hide main window until splash finishes
        self.root.withdraw()

        # Launch animated splash screen
        self.splash = SplashScreen(on_finish=self._on_splash_complete)

    def _center_window(self, width, height):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _on_splash_complete(self):
        # Reveal main window and show login screen
        self.root.deiconify()
        self.show_login()

    def show_login(self):
        self._clear_root()
        self.login_view = LoginWindow(
            self.root,
            on_login_success=self.show_main_dashboard
        )
        self.login_view.pack(fill="both", expand=True)

    def show_main_dashboard(self, user_info):
        self._clear_root()
        self.main_window = MainWindow(
            self.root,
            user_info=user_info,
            on_logout=self.show_login
        )
        self.main_window.pack(fill="both", expand=True)

    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SkyLinkApp()
    app.run()