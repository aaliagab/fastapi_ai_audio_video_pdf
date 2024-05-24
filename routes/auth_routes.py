from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.user_dao import UserDAO
from configurations.config import get_db
import hashlib

router_auth = APIRouter()

@router_auth.post("/authenticate")
def authenticate_user(user_name: str, password: str, db: Session = Depends(get_db)):
    user = UserDAO.get_user_by_username(db, user_name)
    if not user or user.user_password != hashlib.md5(password.encode()).hexdigest():
        print(user.user_password+"        "+hashlib.md5(password.encode()).hexdigest())
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_tokens = [ua.access.accesstoken_id for ua in user.user_accesses]
    return {"access_tokens": access_tokens}
