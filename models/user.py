import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from configurations.config import Base
import datetime

class User(Base):
    __tablename__ = 'user'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, comment='(DC2Type:uuid)')
    user_name = Column(String(255), unique=True, nullable=False)
    user_email = Column(String(255))
    user_phone = Column(String(255))
    user_password = Column(String(255), nullable=False)
    date_add = Column(DateTime, default=datetime.datetime.now)
    date_upd = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    sources = relationship('Source', back_populates='user')
    user_accesses = relationship('UserAccess', back_populates='user')
