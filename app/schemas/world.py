from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from .base import BaseSchema, PaginatedResponse


class WorldBase(BaseSchema):
    """Base world schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="World name")
    system: Optional[str] = Field(default=None, max_length=255, description="Star system")
    geography: Optional[Dict[str, Any]] = Field(default=None, description="Geographic information")
    culture_notes: Optional[str] = Field(default=None, description="Cultural notes")
    technology_level: Optional[str] = Field(default=None, max_length=100, description="Technology level")


class WorldCreate(WorldBase):
    """Schema for creating a new world."""
    
    shard_id: Optional[str] = Field(default=None, description="Associated shard ID")


class WorldUpdate(BaseSchema):
    """Schema for updating a world."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    system: Optional[str] = Field(default=None, max_length=255)
    shard_id: Optional[str] = Field(default=None)
    geography: Optional[Dict[str, Any]] = Field(default=None)
    culture_notes: Optional[str] = Field(default=None)
    technology_level: Optional[str] = Field(default=None, max_length=100)


class WorldResponse(WorldBase):
    """Schema for world response."""
    
    id: str
    shard_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    has_shard: bool
    character_count: int
    book_count: int
    magic_system_count: int
    
    # Related data (optional)
    shard: Optional[Dict[str, Any]] = None
    characters: Optional[List[Dict[str, Any]]] = None
    books: Optional[List[Dict[str, Any]]] = None
    magic_systems: Optional[List[Dict[str, Any]]] = None


class WorldList(BaseSchema):
    """Schema for world list response."""
    
    id: str
    name: str
    system: Optional[str] = None
    technology_level: Optional[str] = None
    has_shard: bool
    character_count: int
    book_count: int
    magic_system_count: int
    created_at: datetime


class WorldDetail(WorldResponse):
    """Schema for detailed world response."""
    
    # Include all relationships
    characters: List[Dict[str, Any]]
    books: List[Dict[str, Any]]
    magic_systems: List[Dict[str, Any]]
    shard: Optional[Dict[str, Any]] = None


class WorldFilters(BaseSchema):
    """Schema for world filters."""
    
    system: Optional[str] = Field(default=None, description="Filter by star system")
    technology_level: Optional[str] = Field(default=None, description="Filter by technology level")
    has_shard: Optional[bool] = Field(default=None, description="Filter by shard presence")
    search: Optional[str] = Field(default=None, description="Search by name")


class WorldStats(BaseSchema):
    """Schema for world statistics."""
    
    total_worlds: int
    worlds_with_shards: int
    worlds_by_system: Dict[str, int]
    worlds_by_technology: Dict[str, int]
    average_characters_per_world: float
    average_books_per_world: float
    average_magic_systems_per_world: float


# Paginated response types
WorldPaginatedResponse = PaginatedResponse[WorldList] 