from .config import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

print("DATABASE URL USED IN DATABASE.PY:", SQLALCHEMY_DATABASE_URL)  # Add this line for debugging

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from app.models.base import Base
    Base.metadata.create_all(bind=engine) 