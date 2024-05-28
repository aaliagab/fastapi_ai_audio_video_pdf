import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from configurations.config import Base
import datetime

class Content(Base):
    __tablename__ = 'content'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, comment='(DC2Type:uuid)')
    source_id = Column(String(36), ForeignKey('source.id'))
    access_id = Column(String(36), ForeignKey('access.accesstoken_id'))
    title = Column(String(255), nullable=False)
    phrase = Column(Text, nullable=False)
    date_add = Column(DateTime, default=datetime.datetime.now)
    date_upd = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    status = Column(Integer, comment='1=activo, 0=inactivo')
    
    source = relationship('Source', back_populates='contents')
    access = relationship('Access', back_populates='contents')
