from pydantic import BaseModel

class UserAccessBase(BaseModel):
    user_id: str
    accesstoken_id: str

class UserAccessCreate(UserAccessBase):
    pass

class UserAccessUpdate(UserAccessBase):
    pass

class UserAccessInDBBase(UserAccessBase):
    class Config:
        orm_mode = True

class UserAccess(UserAccessInDBBase):
    class Config:
        orm_mode = True
        from_attributes = True
    pass
