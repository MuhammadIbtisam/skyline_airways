from sqlalchemy.orm import Session
from data_access.models import Aircraft
from data_access.db_connect import get_db, SessionLocal

class AircraftDAO:
    def get_all_aircrafts(self, db: Session):
        return db.query(Aircraft).all()

    def get_aircraft_by_id(self, db: Session, aircraft_id: int):
        return db.query(Aircraft).filter(Aircraft.id == aircraft_id).first()


    def create_aircraft(db: SessionLocal, aircraft_data: dict):
        db_aircraft = Aircraft(**aircraft_data)
        db.add(db_aircraft)
        db.commit()
        db.refresh(db_aircraft)
        return db_aircraft

    def update_aircraft(self, db: Session, aircraft_id: int, aircraft_data: dict):
        db_aircraft = db.query(Aircraft).filter(Aircraft.id == aircraft_id).first()
        if db_aircraft:
            for key, value in aircraft_data.items():
                setattr(db_aircraft, key, value)
            db.commit()
            db.refresh(db_aircraft)
        return db_aircraft

    def delete_aircraft(self, db: Session, aircraft_id: int):
        db_aircraft = db.query(Aircraft).filter(Aircraft.id == aircraft_id).first()
        if db_aircraft:
            db.delete(db_aircraft)
            db.commit()
            return True
        return False
