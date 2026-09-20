from data_structures.hash_table import HashTable
from DATABASE.db_connection import get_connection


class AuthService:
    """
    Authentication Service managing login and user credentials
    backed by the existing HashTable data structure and SQLite database.
    """
    def __init__(self):
        self.login_system = HashTable(size=20)
        self._init_default_users()
        self._sync_passengers_from_db()

    def _init_default_users(self):
        # Admin account
        self.login_system.insert("admin", "admin123", "Admin")
        # Sample passenger account
        self.login_system.insert("bhavishya", "pass123", "Passenger")
        self.login_system.insert("ananya", "pass123", "Passenger")

    def _sync_passengers_from_db(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT passenger_id, name, phone, email FROM passengers")
            passengers = cur.fetchall()
            conn.close()

            for p_id, name, phone, email in passengers:
                username = name.lower().replace(" ", "")
                # Allow logging in by passenger name or ID
                self.login_system.insert(username, "pass123", "Passenger")
                self.login_system.insert(str(p_id), "pass123", "Passenger")
        except Exception:
            pass

    def authenticate(self, username, password):
        if not username or not password:
            return None
        return self.login_system.verify_login(username.strip(), password.strip())

    def register_user(self, username, password, role="Passenger"):
        if not username or not password:
            return False
        self.login_system.insert(username.strip(), password.strip(), role)
        return True
