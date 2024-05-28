from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pydantic_settings import BaseSettings
from typing import List, Iterator

class Settings(BaseSettings):
    DB_USER: str = "root"
    DB_PASSWORD: str = "usbw"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3307"
    DB_NAME: str = "aicontext"
    ALLOWED_HOSTS: List[str] = ["*"]

settings = Settings()

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
