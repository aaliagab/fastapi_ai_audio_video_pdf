import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from configurations.config import Base
import datetime

class Source(Base):
    __tablename__ = 'source'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, comment='(DC2Type:uuid)')
    source_name = Column(String(255), nullable=False)
    user_id = Column(String(36), ForeignKey('user.id'))
    date_add = Column(DateTime, default=datetime.datetime.now)
    date_upd = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    user = relationship('User', back_populates='sources')
    contents = relationship('Content', back_populates='source')
