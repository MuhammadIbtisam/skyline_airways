from data_access.booking_dao import BookingDAO
from sqlalchemy.orm import Session

class BookingService:
    # def __init__(self, db_name="skyline_airways.db"):
    #     self.booking_dao = BookingDAO(db_name)

    def get_passenger_bookings(self, db: Session, user_id: int):
        reservations = self.booking_dao.get_passenger_reservations(db, user_id)
        bookings = []
        for res in reservations:
            bookings.append({
                "flight_number": res.flight.number,
                "departure_from": res.flight.departure_from,
                "destination": res.flight.destination,
                "departure_time": res.flight.departure_time,
                "seat_no": res.seat_no,
                "status": res.status
            })
        return bookings