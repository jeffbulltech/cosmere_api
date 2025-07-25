"""
Base service with common business logic.
"""
from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
import logging

logger = logging.getLogger(__name__)

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[RepositoryType]):
    """Base service with common business logic."""
    
    def __init__(self, repository: RepositoryType):
        self.repository = repository
    
    def get(self, id: str) -> Optional[Any]:
        """Get a single record by ID."""
        return self.repository.get(id)
    
    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None
    ) -> List[Any]:
        """Get multiple records with pagination and filtering."""
        return self.repository.get_multi(skip=skip, limit=limit, filters=filters, order_by=order_by)
    
    def create(self, obj_in: Dict[str, Any]) -> Optional[Any]:
        """Create a new record with validation."""
        # Add business logic validation here
        return self.repository.create(obj_in)
    
    def update(self, id: str, obj_in: Dict[str, Any]) -> Optional[Any]:
        """Update an existing record with validation."""
        # Add business logic validation here
        return self.repository.update(id, obj_in)
    
    def delete(self, id: str) -> bool:
        """Delete a record with validation."""
        # Add business logic validation here
        return self.repository.delete(id)
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get total count of records."""
        return self.repository.count(filters)
    
    def exists(self, id: str) -> bool:
        """Check if a record exists."""
        return self.repository.exists(id)
    
    def search(self, search_term: str, fields: List[str]) -> List[Any]:
        """Search records by multiple fields."""
        return self.repository.search(search_term, fields)
    
    def get_paginated_response(
        self, 
        items: List[Any], 
        total: int, 
        skip: int, 
        limit: int
    ) -> Dict[str, Any]:
        """Create a paginated response."""
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        } 