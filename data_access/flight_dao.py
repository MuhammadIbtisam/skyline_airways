from sqlalchemy.orm import Session
from data_access.models import Flight, User, CrewFlight
from data_access.db_connect import get_db, SessionLocal

class FlightDAO:
    def get_all_flights(self, db: Session):
        return db.query(Flight).all()

    def get_flight_by_id(db: SessionLocal, flight_id: int):
        return db.query(Flight).filter(Flight.id == flight_id).first()

    def get_flights_by_status(db: SessionLocal, status: str):
        return db.query(Flight).filter(Flight.status == status).all()

    def get_flights_by_departure(db: SessionLocal, departure_from: str):
        return db.query(Flight).filter(Flight.departure_from == departure_from).all()

    def get_flights_by_destination(db: SessionLocal, destination: str):
        return db.query(Flight).filter(Flight.destination == destination).all()

    def get_crew_flights(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.crew_id:
            flights = db.query(Flight).join(CrewFlight).filter(CrewFlight.crew_id == user.crew_id).all()
            return flights
        return []

    def create_flight(db: SessionLocal, flight_data: dict):
        db_flight = Flight(**flight_data)
        db.add(db_flight)
        db.commit()
        db.refresh(db_flight)
        return db_flight

    def update_flight(db: SessionLocal, flight_id: int, flight_data: dict):
        db_flight = db.query(Flight).filter(Flight.id == flight_id).first()
        if db_flight:
            for key, value in flight_data.items():
                setattr(db_flight, key, value)
            db.commit()
            db.refresh(db_flight)
        return db_flight

    def delete_flight(db: SessionLocal, flight_id: int):
        db_flight = db.query(Flight).filter(Flight.id == flight_id).first()
        if db_flight:
            db.delete(db_flight)
            db.commit()
            return True
        return False


# def get_all_flights():
#     return None