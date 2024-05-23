from pydantic import BaseModel
from datetime import datetime

class SourceBase(BaseModel):
    source_name: str
    user_id: str

class SourceCreate(SourceBase):
    pass

class SourceUpdate(SourceBase):
    pass

class SourceInDBBase(SourceBase):
    id: str
    date_add: datetime
    date_upd: datetime

    class Config:
        orm_mode = True

class Source(SourceInDBBase):
    pass
