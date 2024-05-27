from sqlalchemy import or_
from sqlalchemy.orm import Session
from models.content import Content
from sqlalchemy.dialects import mysql
class ContentDAO:
    @staticmethod
    def get_all_contents(db: Session):
        return db.query(Content).all()
    
    @staticmethod
    def get_content_by_id(db: Session, content_id: str):
        return db.query(Content).filter(Content.id == content_id).first()
    
    @staticmethod
    def get_contents_by_user(db: Session, sources: list, access_tokens: list):
        query = db.query(Content).filter(
            or_(
                Content.source_id.in_(sources),
                Content.access_id.in_(access_tokens)
            )
        ).distinct()

        # Imprimir la consulta SQL generada para depuración
        print(query.statement.compile(dialect=mysql.dialect()))
        return query.all()
    
    @staticmethod
    def create_content(db: Session, content: Content):
        db.add(content)
        db.commit()
        db.refresh(content)
        return content
    
    @staticmethod
    def update_content(db: Session, content_id: str, content_data: dict):
        content = db.query(Content).filter(Content.id == content_id).first()
        if content:
            for key, value in content_data.items():
                setattr(content, key, value)
            db.commit()
            db.refresh(content)
        return content
    
    @staticmethod
    def delete_content(db: Session, content_id: str):
        content = db.query(Content).filter(Content.id == content_id).first()
        if content:
            db.delete(content)
            db.commit()
        return content
