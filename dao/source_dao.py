from sqlalchemy.orm import Session
from models.source import Source

class SourceDAO:
    @staticmethod
    def get_all_sources(db: Session):
        return db.query(Source).all()
    
    @staticmethod
    def get_source_by_id(db: Session, source_id: str):
        return db.query(Source).filter(Source.id == source_id).first()
    
    @staticmethod
    def create_source(db: Session, source: Source):
        db.add(source)
        db.commit()
        db.refresh(source)
        return source
    
    @staticmethod
    def update_source(db: Session, source_id: str, source_data: dict):
        source = db.query(Source).filter(Source.id == source_id).first()
        if source:
            for key, value in source_data.items():
                setattr(source, key, value)
            db.commit()
            db.refresh(source)
        return source
    
    @staticmethod
    def delete_source(db: Session, source_id: str):
        source = db.query(Source).filter(Source.id == source_id).first()
        if source:
            db.delete(source)
            db.commit()
        return source
