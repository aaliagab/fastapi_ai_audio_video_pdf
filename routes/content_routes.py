from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.content_dao import ContentDAO
from models.content import Content as SQLAlchemyContent
from dto.content_dto import Content, ContentCreate, ContentUpdate
from configurations.config import get_db
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Content])
def read_contents(db: Session = Depends(get_db)):
    return ContentDAO.get_all_contents(db)

@router.get("/{content_id}", response_model=Content)
def read_content(content_id: str, db: Session = Depends(get_db)):
    content = ContentDAO.get_content_by_id(db, content_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.post("/", response_model=Content)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    db_content = SQLAlchemyContent(**content.dict())
    return ContentDAO.create_content(db, db_content)

@router.put("/{content_id}", response_model=Content)
def update_content(content_id: str, content: ContentUpdate, db: Session = Depends(get_db)):
    content_data = content.dict()
    updated_content = ContentDAO.update_content(db, content_id, content_data)
    if updated_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return updated_content

@router.delete("/{content_id}")
def delete_content(content_id: str, db: Session = Depends(get_db)):
    deleted_content = ContentDAO.delete_content(db, content_id)
    if deleted_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"detail": "Content deleted"}
