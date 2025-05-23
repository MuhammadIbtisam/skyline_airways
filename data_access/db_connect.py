import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from data_access.models import Base


db_path = Path(__file__).resolve().parent.parent / 'database' / 'airline_reservation.db'
DATABASE_URL = f"sqlite:///{db_path.as_posix()}"

# DATABASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.getcwd(), 'database', 'airline_reservation.db')))
# DATABASE_URL = f"sqlite:////{os.path.join(DATABASE_DIR, 'airline_reservation.db')}"

# if not os.path.exists(DATABASE_DIR):
#     os.makedirs(DATABASE_DIR)

db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_session():
    return SessionLocal()