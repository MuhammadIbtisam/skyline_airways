# from sqlalchemy.orm import Session
# from database_layer.database_connection import create_db_engine, create_db_session
# from database_layer.models import Reservation, User, Flight

from sqlalchemy.orm import Session
from data_access.models import Reservation, User, Flight
from data_access.db_connect import get_db, SessionLocal
class BookingDAO:
    # def __init__(self, db_name="skyline_airways.db"):
    #     self.engine = create_db_engine(db_name)
    #     Base.metadata.create_all(self.engine)

    # def get_db(self):
    #     db = create_db_session(self.engine)
    #     try:
    #         yield db
    #     finally:
    #         db.close()

    def get_passenger_reservations(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.passenger_id:
            reservations = db.query(Reservation).filter(Reservation.passenger_id == user.passenger_id).all()
            return reservations
        return []
