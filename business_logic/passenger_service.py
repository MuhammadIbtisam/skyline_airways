from data_access.passenger_dao import PassengerDAO
from data_access.user_dao import UserDAO
from sqlalchemy.orm import Session
import bcrypt

class PassengerService:
    def __init__(self):
        self.passenger_dao = PassengerDAO()
        self.user_dao = UserDAO()

    def sign_up_passenger(self, db: Session, username: str, password: str, first_name: str, last_name: str, email: str,
                          phone: str, passport_number: str, dob: str, nationality: str):
        passenger_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "passport_number": passport_number,
            "dob": dob,
            "nationality": nationality
        }
        passenger_id = self.passenger_dao.create_passenger(db, passenger_data)

        if passenger_id:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            role = 'Passenger'
            success = self.user_dao.insert_user(db, username, hashed_password, role, None, passenger_id)
            if success:
                return passenger_id
            else:
                # If user creation fails, rollback passenger creation
                db.rollback()
                return None
        else:
            return None