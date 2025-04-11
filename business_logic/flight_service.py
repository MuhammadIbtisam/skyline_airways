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

    def create_flight(self, flight_data: dict):
        return self.flight_dao.add_flight(self.db_session, flight_data)

    def update_flight(self, db: Session, flight_id: int, flight_data: dict):
        return self.flight_dao.update_flight(db, flight_id, flight_data)

    def delete_flight(self, db: Session, flight_id: int):
        val = self.flight_dao.delete_flight(db, flight_id)
        return val

    def get_flight_status_counts(self, db: Session):
        return self.flight_dao.get_flight_status_counts(db)