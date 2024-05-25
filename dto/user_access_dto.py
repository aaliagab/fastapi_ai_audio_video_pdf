from pydantic import BaseModel

class UserAccessBase(BaseModel):
    user_id: str
    accesstoken_id: str

class UserAccessCreate(UserAccessBase):
    pass

class UserAccessUpdate(BaseModel):
    user_id: str = None
    accesstoken_id: str = None

class UserAccessInDBBase(UserAccessBase):
    class Config:
        orm_mode = True

class UserAccess(UserAccessInDBBase):
    class Config:
        orm_mode = True
        from_attributes = True
    pass
