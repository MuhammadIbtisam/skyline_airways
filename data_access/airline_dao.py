from dns.e164 import query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from data_access.models import Airline, Aircraft
from data_access.db_connect import get_db, SessionLocal

class AirlineDAO:
    def get_all_airlines(self, db: Session):
        return db.query(Airline).all()

    def get_airline_by_id(self, db: Session, airline_id: int):
        return db.query(Airline).filter(Airline.id == airline_id).first()


    def create_airline(self, db: Session, airline_data: dict):
        db_airline = Airline(**airline_data)
        db.add(db_airline)
        db.commit()
        db.refresh(db_airline)
        return db_airline

    def update_airline(self, db: Session, airline_id: int, airline_data: dict):
        db_airline = db.query(Airline).filter(Airline.id == airline_id).first()
        if db_airline:
            for key, value in airline_data.items():
                setattr(db_airline, key, value)
            db.commit()
            db.refresh(db_airline)
        return db_airline

    def delete_airline(self, db: Session, airline_id: int):
        db_airline = db.query(Airline).filter(Airline.id == airline_id).first()
        print('I am here')
        if db_airline:
            print('I am here 2')
            db.delete(db_airline)
            db.commit()
            return True
        return False

    def get_airline_fleet_size(self, db: Session) -> list:
        try:
            query = select(Airline.name, func.count(Aircraft.id)). \
                outerjoin(Aircraft, Airline.id == Aircraft.airline_id). \
                group_by(Airline.name)
            result = db.execute(query).fetchall()
            return [{"airline_name": row[0], "num_aircraft": row[1]} for row in result]
        except Exception as e:
            print(f"Error fetching airline fleet size: {e}")
            return []

    def get_airline_fleet_capacity(self, db: Session) -> list:
        try:
            query = select(Airline.name, func.sum(Aircraft.capacity)). \
                outerjoin(Aircraft, Airline.id == Aircraft.airline_id). \
                group_by(Airline.name)
            result = db.execute(query).fetchall()
            return [{"airline_name": row[0], "total_capacity": row[1] if row[1] else 0} for row in result]
        except Exception as e:
            print(f"Error fetching total fleet capacity: {e}")
            return []