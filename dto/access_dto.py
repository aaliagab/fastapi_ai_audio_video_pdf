from pydantic import BaseModel

class AccessBase(BaseModel):
    access_name: str

class AccessCreate(AccessBase):
    pass

class AccessUpdate(AccessBase):
    pass

class AccessInDBBase(AccessBase):
    accesstoken_id: str

    class Config:
        orm_mode = True

class Access(AccessInDBBase):
    pass
