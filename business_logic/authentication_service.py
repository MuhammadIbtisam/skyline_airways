# business_logic/authentication_service.py
from data_access.user_dao import UserDAO
from sqlalchemy.orm import Session

class AuthenticationService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register_user(self, db: Session, username: str, password: str, role: str, crew_id: int = None, passenger_id: int = None):
        try:
            return self.user_dao.register_user(db, username, password, role, crew_id, passenger_id)
        except Exception as e:
            print(f"Registration error: {e}")
            return None

    def authenticate_user(self, db: Session, username: str, password: str):
        return self.user_dao.authenticate_user(db, username, password)

    def get_user_role(self, db: Session, user_id: int):
        user = self.user_dao.get_user_by_id(db, user_id)
        return user.role if user else None