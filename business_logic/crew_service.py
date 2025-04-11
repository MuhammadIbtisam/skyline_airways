import bcrypt

from data_access.crew_dao import CrewDAO
from data_access.user_dao import UserDAO
from sqlalchemy.orm import Session

class CrewService:
    def __init__(self):
        self.crew_dao = CrewDAO()
        self.user_dao = UserDAO()

    def list_all_crews(self, db: Session):
        return self.crew_dao.get_all_crews(db)

    # def get_crews_by_status(self, db: Session, status: str):
    #     return self.crew_dao.get_crew_by_status(db, status)

    def get_crew_by_id(self, db: Session, crew_id: int):
        return self.crew_dao.get_crew_by_id(db, crew_id)

    def create_crew(self, db: Session, first_name: str, last_name: str, email: str, phone: str, role: str, username: str, password: str):
        crew_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "role": role
        }

        crew_id =  self.crew_dao.create_crew(db, crew_data)
        if crew_id:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            success = self.user_dao.insert_user(db, username, hashed_password, role, crew_id, None)
            if success:
                return crew_id
            else:
                db.rollback()
                return None
        else:
            return None

    def update_crew(self, db: Session, crew_id: int, crew_data: dict):
        return self.crew_dao.update_crew(db, crew_id, crew_data)

    # def delete_crew(self, db: Session, crew_id: int):
    #     val = self.crew_dao.delete_crew(db, crew_id)
    #     return val
    #
    # def get_crew_status_counts(self, db: Session):
    #     return self.crew_dao.get_crew_status_counts(db)