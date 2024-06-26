from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from dao.user_dao import UserDAO
from models.user import User as SQLAlchemyUser
from dto.user_dto import UserCreate, UserUpdate, UserResponse
from configurations.config import get_db
from typing import List
from utils import get_auth

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    users = UserDAO.get_all_users(db)
    return [UserResponse.from_orm(user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    user = UserDAO.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(user)

@router.post("/", response_model=UserResponse)
def create_user(request: Request, user: UserCreate, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    existing_user = UserDAO.get_user_by_username(db, user.user_name)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = SQLAlchemyUser(**user.dict())
    created_user = UserDAO.create_user(db, db_user)
    return UserResponse.from_orm(created_user)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(request: Request, user_id: str, user: UserUpdate, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    user_data = user.dict()
    updated_user = UserDAO.update_user(db, user_id, user_data)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(updated_user)

@router.delete("/{user_id}")
def delete_user(request: Request, user_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    deleted_user = UserDAO.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
