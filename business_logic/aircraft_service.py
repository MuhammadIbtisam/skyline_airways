from data_access.aircraft_dao import AircraftDAO
from sqlalchemy.orm import Session

class AircraftService:
    def __init__(self):
        self.aircraft_dao = AircraftDAO()

    def list_all_aircrafts(self, db: Session):
        # Corrected: pass the stored database session
        return self.aircraft_dao.get_all_aircrafts(db)

    def get_aircraft_by_id(self, db: Session, aircraft_id: int):
        return self.aircraft_dao.get_aircraft_by_id(db, aircraft_id)

    def create_aircraft(self, db: Session, aircraft_data: dict):
        return self.aircraft_dao.create_aircraft(self.db_session, aircraft_data)

    def update_aircraft(self, db: Session, aircraft_id: int, aircraft_data: dict):
        return self.aircraft_dao.update_aircraft(db, aircraft_id, aircraft_data)

    def delete_aircraft(self, db: Session, aircraft_id: int):
        val = self.aircraft_dao.delete_aircraft(db, aircraft_id)
        return val