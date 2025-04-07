# business_logic/flight_service.py
from data_access.flight_dao import FlightDAO
from sqlalchemy.orm import Session
# from data_access.flight_dao import get_all_flights
# from data_access.flight_dao import get_flight_by_number
# from data_access.flight_dao import add_flight
# from data_access.flight_dao import update_flight
# from data_access.flight_dao import delete_flight

class FlightService:
    def __init__(self):
        self.flight_dao = FlightDAO()

    def list_all_flights(self, db: Session):
        # Corrected: pass the stored database session
        return self.flight_dao.get_all_flights(db)

    def get_flight(self, flight_number: str):
        return flight_dao.get_flight_by_number(self.db_session, flight_number)

    def create_flight(self, flight_data: dict):
        return flight_dao.add_flight(self.db_session, flight_data)

    def update_flight(self, flight_id: int, flight_data: dict):
        return flight_dao.update_flight(self.db_session, flight_id, flight_data)

    def delete_flight(self, flight_id: int):
        return flight_dao.delete_flight(self.db_session, flight_id)