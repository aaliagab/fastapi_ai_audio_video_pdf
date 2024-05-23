from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    user_name: str
    user_email: str
    user_phone: str
    user_password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: str
    date_add: datetime
    date_upd: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass
