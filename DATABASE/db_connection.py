import sqlite3

DATABASE_NAME = "airline.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection