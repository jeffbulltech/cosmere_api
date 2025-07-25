"""
Base repository with common CRUD operations.
"""
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session, Query
from sqlalchemy import and_, or_
from app.models.base import BaseModel
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get(self, id: str) -> Optional[ModelType]:
        """Get a single record by ID."""
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by id {id}: {e}")
            return None
    
    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """Get multiple records with pagination and filtering."""
        try:
            query = self.db.query(self.model)
            
            # Apply filters
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field) and value is not None:
                        if isinstance(value, list):
                            query = query.filter(getattr(self.model, field).in_(value))
                        else:
                            query = query.filter(getattr(self.model, field) == value)
            
            # Apply ordering
            if order_by:
                if hasattr(self.model, order_by):
                    query = query.order_by(getattr(self.model, order_by))
            
            return query.offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting multiple {self.model.__name__}: {e}")
            return []
    
    def create(self, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Create a new record."""
        try:
            db_obj = self.model(**obj_in)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            logger.info(f"Created {self.model.__name__} with id {db_obj.id}")
            return db_obj
        except Exception as e:
            logger.error(f"Error creating {self.model.__name__}: {e}")
            self.db.rollback()
            return None
    
    def update(self, id: str, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Update an existing record."""
        try:
            db_obj = self.get(id)
            if not db_obj:
                return None
            
            for field, value in obj_in.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            self.db.commit()
            self.db.refresh(db_obj)
            logger.info(f"Updated {self.model.__name__} with id {id}")
            return db_obj
        except Exception as e:
            logger.error(f"Error updating {self.model.__name__} with id {id}: {e}")
            self.db.rollback()
            return None
    
    def delete(self, id: str) -> bool:
        """Delete a record by ID."""
        try:
            db_obj = self.get(id)
            if not db_obj:
                return False
            
            self.db.delete(db_obj)
            self.db.commit()
            logger.info(f"Deleted {self.model.__name__} with id {id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting {self.model.__name__} with id {id}: {e}")
            self.db.rollback()
            return False
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get total count of records."""
        try:
            query = self.db.query(self.model)
            
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field) and value is not None:
                        query = query.filter(getattr(self.model, field) == value)
            
            return query.count()
        except Exception as e:
            logger.error(f"Error counting {self.model.__name__}: {e}")
            return 0
    
    def exists(self, id: str) -> bool:
        """Check if a record exists."""
        try:
            return self.db.query(self.model).filter(self.model.id == id).first() is not None
        except Exception as e:
            logger.error(f"Error checking existence of {self.model.__name__} with id {id}: {e}")
            return False
    
    def search(self, search_term: str, fields: List[str]) -> List[ModelType]:
        """Search records by multiple fields."""
        try:
            query = self.db.query(self.model)
            search_filters = []
            
            for field in fields:
                if hasattr(self.model, field):
                    search_filters.append(
                        getattr(self.model, field).ilike(f"%{search_term}%")
                    )
            
            if search_filters:
                query = query.filter(or_(*search_filters))
            
            return query.all()
        except Exception as e:
            logger.error(f"Error searching {self.model.__name__}: {e}")
            return []
    
    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get a record by a specific field value."""
        try:
            if hasattr(self.model, field):
                return self.db.query(self.model).filter(
                    getattr(self.model, field) == value
                ).first()
            return None
        except Exception as e:
            logger.error(f"Error getting {self.model.__name__} by {field}: {e}")
            return None
    
    def get_by_field_multi(self, field: str, value: Any) -> List[ModelType]:
        """Get multiple records by a specific field value."""
        try:
            if hasattr(self.model, field):
                return self.db.query(self.model).filter(
                    getattr(self.model, field) == value
                ).all()
            return []
        except Exception as e:
            logger.error(f"Error getting multiple {self.model.__name__} by {field}: {e}")
            return [] 