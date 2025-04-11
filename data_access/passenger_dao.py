
from sqlalchemy import insert
from sqlalchemy.orm import Session
from .models import Passenger

class PassengerDAO:
    def create_passenger(self, db: Session, passenger_data: dict):
        try:
            db_passenger = Passenger(**passenger_data)
            db.add(db_passenger)
            db.commit()
            db.refresh(db_passenger)
            return db_passenger.id
        except Exception as e:
            db.rollback()
            print(f"Error creating passenger: {e}")
            return None