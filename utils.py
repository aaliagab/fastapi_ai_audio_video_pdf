from dao.access_dao import AccessDAO
from models.access import Access
from sqlalchemy.orm import Session
from dao.user_dao import UserDAO
from models.user import User
from models.user_access import UserAccess
from dao.user_access_dao import UserAccessDAO
from fastapi import HTTPException, Depends
from starlette.requests import Request
from fastapi.security.api_key import APIKeyHeader

api_key_header = APIKeyHeader(name='Authorization', auto_error=False)

def ensure_admin_user(db: Session):
    admin_user = UserDAO.get_user_by_username(db, "admin")
    if not admin_user:
        password = "adminadmin"
        admin_user = User(user_name="admin", user_email="admin@a.aa",user_phone="", user_password=password)
        UserDAO.create_user(db, admin_user)

    admin_access = AccessDAO.get_access_by_name(db, "admin")
    if not admin_access:
        admin_access = Access(access_name="admin")
        AccessDAO.create_access(db, admin_access)
    user_access = UserAccessDAO.get_user_access_by_id(db, admin_user.id, admin_access.accesstoken_id)
    if not user_access:
        user_access = UserAccess(user_id=admin_user.id, accesstoken_id=admin_access.accesstoken_id)
        UserAccessDAO.create_user_access(db, user_access)

def get_auth(api_key: str = Depends(api_key_header)):
    import json
    if not api_key:
        raise HTTPException(status_code=403, detail="No Authorization header found")
    try:
        auth = json.loads(api_key)
        return auth
    except json.JSONDecodeError:
        raise HTTPException(status_code=403, detail="Invalid Authorization header format")
