from dao.access_dao import AccessDAO
from models.access import Access
from sqlalchemy.orm import Session
from dao.user_dao import UserDAO
from models.user import User
from models.user_access import UserAccess
from dao.user_access_dao import UserAccessDAO

def ensure_admin_access(db: Session):
    admin_access = AccessDAO.get_access_by_name(db, "admin")
    if not admin_access:
        admin_access = Access(access_name="admin")
        AccessDAO.create_access(db, admin_access)

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
    user_access = UserAccess(user_id=admin_user.id, accesstoken_id=admin_access.accesstoken_id)
    UserAccessDAO.create_user_access(db, user_access)
