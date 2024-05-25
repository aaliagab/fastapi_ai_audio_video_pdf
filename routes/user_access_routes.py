from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from dao.user_access_dao import UserAccessDAO
from dao.user_dao import UserDAO
from dao.access_dao import AccessDAO
from models.user_access import UserAccess as SQLAlchemyUserAccess
from dto.user_access_dto import UserAccess, UserAccessCreate, UserAccessUpdate
from configurations.config import get_db
from typing import List
from utils import get_auth

router = APIRouter()

@router.get("/", response_model=List[UserAccess])
def read_user_accesses(db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    return UserAccessDAO.get_all_user_accesses(db)

@router.get("/{user_id}/{access_id}", response_model=UserAccess)
def read_user_access(user_id: str, access_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    user_access = UserAccessDAO.get_user_access_by_id(db, user_id, access_id)
    if user_access is None:
        raise HTTPException(status_code=404, detail="User Access not found")
    return user_access

@router.post("/", response_model=UserAccess)
def create_user_access(request: Request, user_access: UserAccessCreate, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    # Verificar si el user_id y access_id existen
    if not UserDAO.get_user_by_id(db, user_access.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not AccessDAO.get_access_by_id(db, user_access.accesstoken_id):
        raise HTTPException(status_code=404, detail="Access token not found")

    db_user_access = SQLAlchemyUserAccess(**user_access.dict())
    return UserAccessDAO.create_user_access(db, db_user_access)

@router.put("/{user_id}/{access_id}", response_model=UserAccess)
def update_user_access(request: Request, user_id: str, access_id: str, user_access: UserAccessUpdate, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    # Verificar si el user_access actual existe
    existing_user_access = UserAccessDAO.get_user_access_by_id(db, user_id, access_id)
    if not existing_user_access:
        raise HTTPException(status_code=404, detail="User Access not found")

    user_access_data = user_access.dict(exclude_unset=True)

    # Verificar si el nuevo user_id existe
    new_user_id = user_access_data.get('user_id')
    if new_user_id and not UserDAO.get_user_by_id(db, new_user_id):
        raise HTTPException(status_code=404, detail="New user not found")
    
    # Verificar si el nuevo access_id existe
    new_access_id = user_access_data.get('accesstoken_id')
    if new_access_id and not AccessDAO.get_access_by_id(db, new_access_id):
        raise HTTPException(status_code=404, detail="New access token not found")

    updated_user_access = UserAccessDAO.update_user_access(db, user_id, access_id, user_access_data)
    if updated_user_access is None:
        raise HTTPException(status_code=404, detail="User Access not found")
    return updated_user_access

@router.delete("/{user_id}/{access_id}")
def delete_user_access(request: Request, user_id: str, access_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    user_access = UserAccessDAO.delete_user_access(db, user_id, access_id)
    if user_access is None:
        raise HTTPException(status_code=404, detail="User Access not found")
    return {"detail": "User Access deleted"}
