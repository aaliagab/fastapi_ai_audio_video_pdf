from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.user_dao import UserDAO
from configurations.config import get_db
from starlette.requests import Request
import hashlib

router_auth = APIRouter()

@router_auth.post("/authenticate")
def authenticate_user(request: Request, user_name: str, password: str, db: Session = Depends(get_db)):
    user = UserDAO.get_user_by_username(db, user_name)
    if not user or user.user_password != hashlib.md5(password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_tokens = [ua.access.accesstoken_id for ua in user.user_accesses]
    sources = [us.id for us in user.sources]
    request.state.user = user
    request.state.access_tokens = access_tokens
    request.state.sources = sources
    return {
        "message": "Authentication successful",
        "auth": {
            "access_tokens": access_tokens,
            "sources": sources,
            "user_id": user.id,
            "user_name": user.user_name
        }
    }
