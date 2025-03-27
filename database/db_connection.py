import sqlite3
import os

DB_NAME = "airline_reservation.db"

def init_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    else:
        from database.initialize_db import initialize_db
        initialize_db()

def get_db_connection():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
