from dao.user_access_dao import UserAccessDAO
from dao.access_dao import AccessDAO
from fastapi import Depends, HTTPException
from configurations.config import get_db
from sqlalchemy.orm import Session

def has_admin_access(user_id: str, db: Session = Depends(get_db)):
    admin_access = AccessDAO.get_access_by_name(db, "admin")
    if not admin_access:
        raise HTTPException(status_code=500, detail="Admin access not found")

    user_access = UserAccessDAO.get_user_access_by_id(db, user_id, admin_access.accesstoken_id)
    if not user_access:
        raise HTTPException(status_code=403, detail="Access denied. Admin role required.")
