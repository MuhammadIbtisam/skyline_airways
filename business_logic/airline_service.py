from data_access.airline_dao import AirlineDAO
from sqlalchemy.orm import Session

class AirlineService:
    def __init__(self):
        self.airline_dao = AirlineDAO()

    def list_all_airlines(self, db: Session):
        # Corrected: pass the stored database session
        return self.airline_dao.get_all_airlines(db)

    def get_airline_by_id(self, db: Session, airline_id: int):
        return self.airline_dao.get_airline_by_id(db, airline_id)

    def create_airline(self, db: Session, airline_data: dict):
        return self.airline_dao.create_airline(db, airline_data)

    def update_airline(self, db: Session, airline_id: int, airline_data: dict):
        return self.airline_dao.update_airline(db, airline_id, airline_data)

    def delete_airline(self, db: Session, airline_id: int):
        return self.airline_dao.delete_airline(db, airline_id)

    def get_airline_fleet_size(self, db: Session):
        return self.airline_dao.get_airline_fleet_size(db)

    def get_total_fleet_capacity(self, db: Session):
        return self.airline_dao.get_airline_fleet_capacity(db)