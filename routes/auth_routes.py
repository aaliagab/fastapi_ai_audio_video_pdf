from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.user_dao import UserDAO
from dao.user_access_dao import UserAccessDAO
from configurations.config import get_db

router_auth = APIRouter()

@router_auth.post("/authenticate")
def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user = UserDAO.get_user_by_email(db, email)
    if not user or user.user_password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_tokens = [ua.access.accesstoken_id for ua in user.user_accesses]
    return {"access_tokens": access_tokens}
