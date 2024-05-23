from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.user_access_dao import UserAccessDAO
from models.user_access import UserAccess as SQLAlchemyUserAccess
from dto.user_access_dto import UserAccess, UserAccessCreate, UserAccessUpdate
from configurations.config import get_db
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserAccess])
def read_user_accesses(db: Session = Depends(get_db)):
    return UserAccessDAO.get_all_user_accesses(db)

@router.get("/{user_id}/{access_id}", response_model=UserAccess)
def read_user_access(user_id: str, access_id: str, db: Session = Depends(get_db)):
    user_access = UserAccessDAO.get_user_access_by_id(db, user_id, access_id)
    if user_access is None:
        raise HTTPException(status_code=404, detail="User Access not found")
    return user_access

@router.post("/", response_model=UserAccess)
def create_user_access(user_access: UserAccessCreate, db: Session = Depends(get_db)):
    db_user_access = SQLAlchemyUserAccess(**user_access.dict())
    return UserAccessDAO.create_user_access(db, db_user_access)

@router.put("/{user_id}/{access_id}", response_model=UserAccess)
def update_user_access(user_id: str, access_id: str, user_access: UserAccessUpdate, db: Session = Depends(get_db)):
    user_access_data = user_access.dict()
    updated_user_access = UserAccessDAO.update_user_access(db, user_id, access_id, user_access_data)
    if updated_user_access is None:
        raise HTTPException(status_code=404, detail="User Access not found")
    return updated_user_access

@router.delete("/{user_id}/{access_id}")
def delete_user_access(user_id: str, access_id: str, db: Session = Depends(get_db)):
    user_access = UserAccessDAO.delete_user_access(db, user_id, access_id)
    if user_access is None:
        raise HTTPException(status_code=404, detail="User Access not found")
    return {"detail": "User Access deleted"}
