from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.access_dao import AccessDAO
from models.access import Access as SQLAlchemyAccess
from dto.access_dto import Access, AccessCreate, AccessUpdate
from configurations.config import get_db
from typing import List
from dependencies import has_admin_access

router = APIRouter()


@router.get("/", response_model=List[Access], dependencies=[Depends(has_admin_access)])
def read_accesses(db: Session = Depends(get_db)):
    return AccessDAO.get_all_accesses(db)

@router.get("/{access_id}", response_model=Access)
def read_access(access_id: str, db: Session = Depends(get_db)):
    access = AccessDAO.get_access_by_id(db, access_id)
    if access is None:
        raise HTTPException(status_code=404, detail="Access not found")
    return access

@router.post("/", response_model=Access)
def create_access(access: AccessCreate, db: Session = Depends(get_db)):
    db_access = SQLAlchemyAccess(**access.dict())
    return AccessDAO.create_access(db, db_access)

@router.put("/{access_id}", response_model=Access)
def update_access(access_id: str, access: AccessUpdate, db: Session = Depends(get_db)):
    access_data = access.dict()
    updated_access = AccessDAO.update_access(db, access_id, access_data)
    if updated_access is None:
        raise HTTPException(status_code=404, detail="Access not found")
    return updated_access

@router.delete("/{access_id}")
def delete_access(access_id: str, db: Session = Depends(get_db)):
    deleted_access = AccessDAO.delete_access(db, access_id)
    if deleted_access is None:
        raise HTTPException(status_code=404, detail="Access not found")
    return {"detail": "Access deleted"}
