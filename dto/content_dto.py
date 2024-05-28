from pydantic import BaseModel
from datetime import datetime

class ContentBase(BaseModel):
    source_id: str
    access_id: str
    title: str
    phrase: str
    status: int

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    pass

class ContentInDBBase(ContentBase):
    id: str
    date_add: datetime
    date_upd: datetime

    class Config:
        orm_mode = True

class Content(ContentInDBBase):
    pass
