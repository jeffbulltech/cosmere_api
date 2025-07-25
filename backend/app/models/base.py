"""
Base model with common fields and methods.
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr
import uuid

Base = declarative_base()


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BaseModel(Base, TimestampMixin):
    """Base model with common fields and methods."""
    
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        """Generate table name from class name."""
        return cls.__name__.lower() + 's'
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result
    
    def update(self, **kwargs):
        """Update model instance with provided kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    @classmethod
    def get_by_id(cls, db, id):
        """Get model instance by ID."""
        return db.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def get_all(cls, db, skip=0, limit=100):
        """Get all model instances with pagination."""
        return db.query(cls).offset(skip).limit(limit).all()
    
    @classmethod
    def count(cls, db):
        """Get total count of model instances."""
        return db.query(cls).count()