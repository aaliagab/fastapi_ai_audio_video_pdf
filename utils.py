from dao.access_dao import AccessDAO
from models.access import Access
from sqlalchemy.orm import Session
import hashlib
from dao.user_dao import UserDAO
from models.user import User

def ensure_admin_access(db: Session):
    admin_access = AccessDAO.get_access_by_name(db, "admin")
    if not admin_access:
        admin_access = Access(access_name="admin")
        AccessDAO.create_access(db, admin_access)

def ensure_admin_user(db: Session):
    admin_user = UserDAO.get_user_by_username(db, "admin")
    if not admin_user:
        password = hashlib.md5("adminadmin".encode()).hexdigest()
        admin_user = User(user_name="admin", user_email="admin@a.aa",user_phone="", user_password=password)
        UserDAO.create_user(db, admin_user)
