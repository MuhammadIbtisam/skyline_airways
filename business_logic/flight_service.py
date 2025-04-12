from datetime import datetime

from data_access.flight_dao import FlightDAO
from sqlalchemy.orm import Session

class FlightService:
    def __init__(self):
        self.flight_dao = FlightDAO()

    def list_all_flights(self, db: Session):
        # Corrected: pass the stored database session
        return self.flight_dao.get_all_flights(db)

    def get_flights_by_status(self, db: Session, status: str):
        return self.flight_dao.get_flight_by_status(db, status)

    def get_flight_by_id(self, db: Session, flight_id: int):
        return self.flight_dao.get_flight_by_id(db, flight_id)

    def get_flight_by_number(self, db: Session, flight_number: str):
        return self.flight_dao.get_flight_by_number(db, flight_number)

    def create_flight(self, db: Session, flight_data: dict):
        return self.flight_dao.create_flight(db, flight_data)

    def update_flight(self, db: Session, flight_id: int, flight_data: dict):
        return self.flight_dao.update_flight(db, flight_id, flight_data)

    def delete_flight(self, db: Session, flight_id: int):
        val = self.flight_dao.delete_flight(db, flight_id)
        return val

    def get_flight_status_counts(self, db: Session):
        return self.flight_dao.get_flight_status_counts(db)

    def get_flight_schedule_for_crew(self, db: Session, crew_id: int):
        return self.flight_dao.get_flight_schedule_for_crew(db, crew_id)

    def update_flight_status(self, db: Session, flight_number: str, new_status: str):
        flight = self.flight_dao.get_flight_by_number(db, flight_number)
        if not flight:
            return False, f"Flight with number {flight_number} not found."
        try:
            update_data = {"status": new_status, "updated_at": datetime.now()}
            self.flight_dao.update_flight(db, flight.id, update_data)
            db.commit()
            return True, None
        except Exception as e:
            db.rollback()
            return False, f"Error updating flight status for {flight_number}: {e}"

