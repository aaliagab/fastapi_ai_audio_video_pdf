from sqlalchemy.orm import Session
from models.user_access import UserAccess

class UserAccessDAO:
    @staticmethod
    def get_all_user_accesses(db: Session):
        return db.query(UserAccess).all()
    
    @staticmethod
    def get_user_access_by_id(db: Session, user_id: str, access_id: str):
        return db.query(UserAccess).filter(UserAccess.user_id == user_id, UserAccess.accesstoken_id == access_id).first()
    
    @staticmethod
    def create_user_access(db: Session, user_access: UserAccess):
        db.add(user_access)
        db.commit()
        db.refresh(user_access)
        return user_access
    
    @staticmethod
    def delete_user_access(db: Session, user_id: str, access_id: str):
        user_access = db.query(UserAccess).filter(UserAccess.user_id == user_id, UserAccess.accesstoken_id == access_id).first()
        if user_access:
            db.delete(user_access)
            db.commit()
        return user_access
