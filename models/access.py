import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from configurations.config import Base

class Access(Base):
    __tablename__ = 'access'
    
    accesstoken_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), comment='(DC2Type:uuid)')
    access_name = Column(String(255), unique=True, nullable=False)
    
    contents = relationship('Content', back_populates='access')
    user_accesses = relationship('UserAccess', back_populates='access')
