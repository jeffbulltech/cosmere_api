from sqlalchemy import Column, String, DateTime, func, Text
from sqlalchemy.ext.declarative import declared_attr
from app.core.database import Base
import uuid
import json
from datetime import datetime


class BaseModel(Base):
    """Base model class with common fields and functionality."""
    
    __abstract__ = True
    
    # Primary key
    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    
    # Timestamps
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    @declared_attr
    def __tablename__(cls):
        """Generate table name from class name."""
        return cls.__name__.lower() + 's'
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            elif isinstance(value, uuid.UUID):
                result[column.name] = str(value)
            elif isinstance(value, str) and self._is_json_field(column.name):
                # Try to deserialize JSON strings
                try:
                    result[column.name] = json.loads(value) if value else None
                except (json.JSONDecodeError, TypeError):
                    result[column.name] = value
            else:
                result[column.name] = value
        return result
    
    def _is_json_field(self, field_name: str) -> bool:
        """Check if a field should be treated as JSON."""
        json_fields = [
            'geography', 'culture_notes', 'mechanics', 'limitations',
            'magic_abilities', 'affiliations', 'cosmere_significance',
            'splinter_info', 'biography'
        ]
        return field_name in json_fields
    
    def update(self, **kwargs):
        """Update model instance with provided fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self
    
    @classmethod
    def get_by_id(cls, db, id: str):
        """Get model instance by ID."""
        return db.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def get_all(cls, db, skip: int = 0, limit: int = 100):
        """Get all model instances with pagination."""
        return db.query(cls).offset(skip).limit(limit).all()
    
    @classmethod
    def count(cls, db):
        """Get total count of model instances."""
        return db.query(cls).count()
    
    def __repr__(self):
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>" 