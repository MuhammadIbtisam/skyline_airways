from sqlalchemy.orm import Session
from data_access.models import Flight, User, CrewFlight, Aircraft, Airline, Reservation, Ticket
from data_access.db_connect import get_db, SessionLocal
from sqlalchemy import select, func

class FlightDAO:
    def get_all_flights(self, db: Session):
        return db.query(Flight).all()

    def get_flight_by_id(self, db: Session, flight_id: int):
        return db.query(Flight).filter(Flight.id == flight_id).first()

    def get_flight_by_status(self, db: Session, status: str):
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

    def update_flight(self, db: Session, flight_id: int, flight_data: dict):
        db_flight = db.query(Flight).filter(Flight.id == flight_id).first()
        if db_flight:
            for key, value in flight_data.items():
                setattr(db_flight, key, value)
            db.commit()
            db.refresh(db_flight)
        return db_flight

    def delete_flight(self, db: Session, flight_id: int):
        db_flight = db.query(Flight).filter(Flight.id == flight_id).first()
        print('I am here')
        if db_flight:
            print('I am here 2')
            db.delete(db_flight)
            db.commit()
            return True
        return False

    def get_flight_status_counts(self, db: Session) -> list:
        try:
            query = select(Flight.status, func.count(Flight.id)). \
                group_by(Flight.status)
            result = db.execute(query).fetchall()
            return [{"status": row[0], "count": row[1]} for row in result]
        except Exception as e:
            print(f"Error fetching flight status counts: {e}")
            return []

    def get_total_revenue_per_airline(self, db: Session):
        try:
            query = select(
                Airline.name.label('airline_name'),
                func.sum(Ticket.price).label('total_revenue')
            ). \
                join(Aircraft, Airline.id == Aircraft.airline_id). \
                join(Flight, Aircraft.id == Flight.aircraft_id). \
                join(Reservation, Flight.id == Reservation.flight_id). \
                join(Ticket, Reservation.id == Ticket.reservation_id). \
                group_by(Airline.name)

            result = db.execute(query).fetchall()
            print(len(result))
            print('I am here')
            return [{"airline_name": row.airline_name,
                     "total_revenue": float(row.total_revenue) if row.total_revenue else 0.0} for row in result]
        except Exception as e:
            print(f"Error fetching total revenue per airline (corrected): {e}")
            return []

    def get_passenger_traffic_by_route(self, db: Session):
        try:
            query = select(
                Flight.departure_from,
                Flight.destination,
                func.count(Reservation.passenger_id).label('passenger_count')
            ). \
                join(Reservation, Flight.id == Reservation.flight_id). \
                group_by(Flight.departure_from, Flight.destination)

            result = db.execute(query).fetchall()
            return [{"departure_from": row[0], "destination": row[1], "passenger_count": row.passenger_count} for row in
                    result]
        except Exception as e:
            print(f"Error fetching passenger traffic by route: {e}")
            return []
