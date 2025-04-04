import sqlite3
import os

DB_NAME = "airline_reservation.db"
SCHEMA_FILE = 'schema.sql'
DEMO_DATA_FILE = "demo_data.sql"

def init_db():
    db_exists = os.path.exists(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if not db_exists:
        print("DB does not exists Creating DB")

        with open(SCHEMA_FILE, 'r') as schema_file:
            schema_sql = schema_file.read()
            conn.executescript(schema_sql)
            print("DB schema created.")

    else:
        print("DBse exists.Clearing Data.")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name};")
            print(f"Cleared data from table: {table_name}")

    if os.path.exists(DEMO_DATA_FILE):
        with open(DEMO_DATA_FILE, 'r') as demo_file:
            demo_sql = demo_file.read()
            conn.executescript(demo_sql)
            print("Data loaded")
    else:
        print("No demo data exists.")

    conn.commit()
    conn.close()

def get_db_connection():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
