from sqlalchemy.orm import Session
from models.access import Access

class AccessDAO:
    @staticmethod
    def get_all_accesses(db: Session):
        return db.query(Access).all()
    
    @staticmethod
    def get_access_by_id(db: Session, access_id: str):
        return db.query(Access).filter(Access.accesstoken_id == access_id).first()
    
    @staticmethod
    def get_access_by_name(db: Session, access_name: str):
        return db.query(Access).filter(Access.access_name == access_name).first()
    
    @staticmethod
    def create_access(db: Session, access: Access):
        db.add(access)
        db.commit()
        db.refresh(access)
        return access
    
    @staticmethod
    def update_access(db: Session, access_id: str, access_data: dict):
        access = db.query(Access).filter(Access.accesstoken_id == access_id).first()
        if access:
            for key, value in access_data.items():
                setattr(access, key, value)
            db.commit()
            db.refresh(access)
        return access
    
    @staticmethod
    def delete_access(db: Session, access_id: str):
        access = db.query(Access).filter(Access.accesstoken_id == access_id).first()
        if access:
            db.delete(access)
            db.commit()
        return access
