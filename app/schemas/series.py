from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from .base import BaseSchema, PaginatedResponse


class SeriesBase(BaseSchema):
    """Base series schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Series name")
    description: Optional[str] = Field(default=None, description="Series description")


class SeriesCreate(SeriesBase):
    """Schema for creating a new series."""
    pass


class SeriesUpdate(BaseSchema):
    """Schema for updating a series."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)


class SeriesResponse(SeriesBase):
    """Schema for series response."""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    book_count: int
    total_word_count: int
    worlds: List[Dict[str, Any]]


class SeriesList(BaseSchema):
    """Schema for series list response."""
    
    id: str
    name: str
    description: Optional[str] = None
    book_count: int
    total_word_count: int
    created_at: datetime


class SeriesDetail(SeriesResponse):
    """Schema for detailed series response."""
    
    # Include all relationships
    books: List[Dict[str, Any]]
    worlds: List[Dict[str, Any]]


# Paginated response types
SeriesPaginatedResponse = PaginatedResponse[SeriesList] 