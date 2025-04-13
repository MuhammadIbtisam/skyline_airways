
from sqlalchemy import insert, select, func
from sqlalchemy.orm import Session
from .models import Passenger, Reservation, Flight

class PassengerDAO:
    def create_passenger(self, db: Session, passenger_data: dict):
        try:
            db_passenger = Passenger(**passenger_data)
            db.add(db_passenger)
            db.commit()
            db.refresh(db_passenger)
            return db_passenger.id
        except Exception as e:
            db.rollback()
            print(f"Error creating passenger: {e}")
            return None
    #
    #
    # def get_passenger_reservations(self, db: Session, passenger_id: int):
    #     try:
    #         query = select(
    #             Flight.number,
    #             Reservation.seat_no,
    #             Reservation.status,
    #             Reservation.booking_date
    #         ). \
    #             join(Reservation, Passenger.id == Reservation.passenger_id). \
    #             join(Flight, Reservation.id == Reservation.flight_id). \
    #             where(Passenger.id == passenger_id)
    #
    #         result = db.execute(query).fetchall()
    #         return [{"departure_from": row[0], "destination": row[1], "passenger_count": row.passenger_count} for row in
    #                 result]
    #     except Exception as e:
    #         print(f"Error fetching passenger traffic by route: {e}")
    #         return []