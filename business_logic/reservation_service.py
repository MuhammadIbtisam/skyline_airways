from data_access.flight_dao import FlightDAO
from data_access.reservation_dao import ReservationDAO
from sqlalchemy.orm import Session
from typing import Tuple, Optional, List, Dict


class ReservationService:
    def __init__(self):
        self.reservation_dao = ReservationDAO()

    def get_passenger_reservations(self, db: Session, passenger_id: int):
        try:
            reservations = self.reservation_dao.get_passenger_reservations(db, passenger_id)
            return reservations, None
        except Exception as e:
            return None, f"Error fetching passenger reservations: {e}"

    def reserve_seat(self, db: Session, reservation_data: dict):
        return self.reservation_dao.book_reservation(db, reservation_data)
