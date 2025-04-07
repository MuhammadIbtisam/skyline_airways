# database/db_connection.py
import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(PROJECT_ROOT, "database", "airline_reservation.db")
SCHEMA_FILE = os.path.join(PROJECT_ROOT, "database", "schema.sql")
DEMO_DATA_FILE = os.path.join(PROJECT_ROOT, "database", "demo_data.sql")

Base = declarative_base()
engine = create_engine(f"sqlite:///{DB_NAME}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db_exists = os.path.exists(DB_NAME)

    conn_sqlite = sqlite3.connect(DB_NAME)
    cursor_sqlite = conn_sqlite.cursor()

    try:
        with open(SCHEMA_FILE, 'r') as schema_file:
            schema_sql = schema_file.read()
            conn_sqlite.executescript(schema_sql)
            print("DB schema created (using sqlite3).")
    except FileNotFoundError as e:
        print(f"Error opening schema file: {e}")
        raise

    if db_exists:
        print("Database exists. Clearing Data (using sqlite3).")
        cursor_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor_sqlite.fetchall()
        for table in tables:
            table_name = table[0]
            cursor_sqlite.execute(f"DELETE FROM {table_name};")
            print(f"Cleared data from table: {table_name}")

    if os.path.exists(DEMO_DATA_FILE):
        with open(DEMO_DATA_FILE, 'r') as demo_file:
            demo_sql = demo_file.read()
            conn_sqlite.executescript(demo_sql)
            print("Demo data loaded (using sqlite3).")
    else:
        print("No demo data exists.")

    conn_sqlite.commit()
    conn_sqlite.close()

    Base.metadata.create_all(bind=engine) # Initialize SQLAlchemy metadata (won't recreate if tables exist)
    print("SQLAlchemy metadata initialized.")

if __name__ == "__main__":
    init_db()