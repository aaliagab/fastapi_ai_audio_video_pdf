from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.user_dao import UserDAO
from models.user import User as SQLAlchemyUser
from dto.user_dto import User, UserCreate, UserUpdate
from configurations.config import get_db
from typing import List

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(db: Session = Depends(get_db)):
    return UserDAO.get_all_users(db)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = UserDAO.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = SQLAlchemyUser(**user.dict())
    return UserDAO.create_user(db, db_user)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    user_data = user.dict()
    updated_user = UserDAO.update_user(db, user_id, user_data)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    deleted_user = UserDAO.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
