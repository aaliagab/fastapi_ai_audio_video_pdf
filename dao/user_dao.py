from sqlalchemy.orm import Session
from models.user import User
import hashlib

class UserDAO:
    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, user_name: str):
        return db.query(User).filter(User.user_name == user_name).first()

    @staticmethod
    def create_user(db: Session, user: User):
        user.user_password = hashlib.md5(user.user_password.encode()).hexdigest()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: str, user_data: dict):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in user_data.items():
                if key == "user_password":
                    value = hashlib.md5(value.encode()).hexdigest()
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: str):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return user
