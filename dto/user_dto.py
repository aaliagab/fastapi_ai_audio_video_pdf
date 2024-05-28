from pydantic import BaseModel
from datetime import datetime
from dto.source_dto import Source
from dto.user_access_dto import UserAccess
from typing import List

class UserBase(BaseModel):
    user_name: str
    user_email: str
    user_phone: str

class UserCreate(UserBase):
    user_password: str

class UserUpdate(BaseModel):
    user_email: str
    user_phone: str
    user_password: str

class UserInDBBase(UserBase):
    id: str
    date_add: datetime
    date_upd: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    user_password: str

class UserResponse(UserInDBBase):
    sources: List[Source]
    user_accesses: List[UserAccess]
    class Config:
        orm_mode = True
        from_attributes = True
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            user_name=obj.user_name,
            user_email=obj.user_email,
            user_phone=obj.user_phone,
            date_add=obj.date_add,
            date_upd=obj.date_upd,
            sources=[Source.from_orm(source) for source in obj.sources],
            user_accesses=[UserAccess.from_orm(user_access) for user_access in obj.user_accesses]
        )
