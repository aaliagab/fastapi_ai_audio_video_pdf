from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from dao.source_dao import SourceDAO
from models.source import Source as SQLAlchemySource
from dto.source_dto import Source, SourceCreate, SourceUpdate
from configurations.config import get_db
from typing import List
from utils import get_auth

router = APIRouter()

@router.get("/", response_model=List[Source])
def read_sources(db: Session = Depends(get_db)):
    return SourceDAO.get_all_sources(db)

@router.get("/{source_id}", response_model=Source)
def read_source(source_id: str, db: Session = Depends(get_db)):
    source = SourceDAO.get_source_by_id(db, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@router.post("/", response_model=Source)
def create_source(request: Request, source: SourceCreate, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    db_source = SQLAlchemySource(**source.dict())
    return SourceDAO.create_source(db, db_source)

@router.put("/{source_id}", response_model=Source)
def update_source(request: Request, source_id: str, source: SourceUpdate, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    source_data = source.dict()
    updated_source = SourceDAO.update_source(db, source_id, source_data)
    if updated_source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return updated_source

@router.delete("/{source_id}")
def delete_source(request: Request, source_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    deleted_source = SourceDAO.delete_source(db, source_id)
    if deleted_source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"detail": "Source deleted"}
