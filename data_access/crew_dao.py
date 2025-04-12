from sqlalchemy.orm import Session
from data_access.models import Crew, CrewFlight, Flight
from data_access.db_connect import get_db, SessionLocal
from sqlalchemy import select, func

class CrewDAO:
    def get_all_crews(self, db: Session):
        return db.query(Crew).all()

    def update_crew(self, db: Session, crew_id: int, crew_data: dict):
        db_crew = db.query(Crew).filter(Crew.id == crew_id).first()
        if db_crew:
            for key, value in crew_data.items():
                if hasattr(db_crew, key):
                    setattr(db_crew, key, value)
            db.commit()
            db.refresh(db_crew)
            return True
        return False

    def get_crew_by_id(self, db: Session, crew_id: int):
        return db.query(Crew).filter(Crew.id == crew_id).first()

    def create_crew(self, db: Session, crew_data: dict):
        db_crew = Crew(**crew_data)
        db.add(db_crew)
        db.commit()
        db.refresh(db_crew)
        return db_crew.id

    def get_flight_schedule_for_crew(self, db: Session, crew_id: int):
        try:
            flights = (db.query(Flight)
                       .join(CrewFlight, Flight.id == CrewFlight.flight_id)
                       .filter(CrewFlight.crew_id == crew_id)
                       .all())
            return flights
        except Exception as e:
            print(f"Error getting flight schedule for crew {crew_id}: {e}")
            return []