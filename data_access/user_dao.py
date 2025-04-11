
import bcrypt
from sqlalchemy import insert
from sqlalchemy.orm import Session
from .models import User, Crew

class UserDAO:
    def get_user_by_username(self, db: Session, username: str):
        print('I am here')
        print(username)
        user = db.query(User).filter(User.username.ilike(username.strip())).first()
        print("User from DB:", user)
        return user

    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def register_user(self, db: Session, username: str, password: str, role: str, crew_id: int = None, passenger_id: int = None):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db_user = User(username=username, hashed_password=hashed_password, role=role, crew_id=crew_id, passenger_id=passenger_id)
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception as e:
            db.rollback()
            raise

    def authenticate_user(self, db: Session, username: str, password: str):
        user = self.get_user_by_username(db, username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            print("User registered successfully")
            return user
        return None

    def update_user(self, db: Session, user_id: int, user_data: dict):
        db_user = self.get_user_by_id(db, user_id)
        if db_user:
            for key, value in user_data.items():
                if key == 'password':
                    hashed_password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    setattr(db_user, 'hashed_password', hashed_password)
                else:
                    setattr(db_user, key, value)
            try:
                db.commit()
                db.refresh(db_user)
                return db_user
            except Exception as e:
                db.rollback()
                raise
        return None

    def delete_user(self, db: Session, user_id: int):
        db_user = self.get_user_by_id(db, user_id)
        if db_user:
            try:
                db.delete(db_user)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise
        return False

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def get_users_by_role(self, db: Session, role: str):
        return db.query(User).filter(User.role == role).all()

    def insert_user(self, db: Session, username: str, hashed_password: str, role: str, crew_id: int, passenger_id: int):
        try:
            stmt = insert(User).values(
                username=username,
                hashed_password=hashed_password,
                role=role,
                crew_id=crew_id,
                passenger_id= passenger_id
            )
            db.execute(stmt)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error inserting user for crew: {e}")
            return False