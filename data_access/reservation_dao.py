from sqlalchemy import insert, select, func
from sqlalchemy.orm import Session
from .models import Passenger, Reservation, Flight


class ReservationDAO:


    def get_passenger_reservations(self, db: Session, passenger_id: int):
        try:
            query = select(
                Flight.number.label("flight_number"),
                Flight.departure_from.label("departure_from"),
                Flight.destination.label("destination"),
                Flight.departure_time.label("departure_time"),
                Flight.arrival_time.label("arrival_time"),
                Reservation.seat_no.label("seat_no"),
                Reservation.status.label("status"),
                Reservation.booking_date.label("booking_date")
            ). \
                join(Passenger, Passenger.id == Reservation.passenger_id). \
                join(Flight, Flight.id == Reservation.flight_id). \
                where(Passenger.id == passenger_id)

            result = db.execute(query).fetchall()
            return [
                {
                    "flight_number": row.flight_number,
                    "departure_from": row.departure_from,
                    "destination": row.destination,
                    "departure_time": row.departure_time,
                    "arrival_time": row.arrival_time,
                    "seat_no": row.seat_no,
                    "status": row.status,
                    "booking_date": row.booking_date,
                }
                for row in result
            ]
        except Exception as e:
            print(f"Error fetching passenger reservations: {e}")
            return []


    def book_reservation(self, db: Session, reservation_data: dict):
        db_reservation = Reservation(**reservation_data)
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation