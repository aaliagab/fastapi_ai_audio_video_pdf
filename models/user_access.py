from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from configurations.config import Base

class UserAccess(Base):
    __tablename__ = 'useraccess'
    
    user_id = Column(String(36), ForeignKey('user.id'), primary_key=True)
    accesstoken_id = Column(String(36), ForeignKey('access.accesstoken_id'), primary_key=True)
    
    user = relationship('User', back_populates='user_accesses')
    access = relationship('Access', back_populates='user_accesses')
