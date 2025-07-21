from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from .base import BaseSchema, PaginatedResponse


class MagicSystemBase(BaseSchema):
    """Base magic system schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Magic system name")
    type: str = Field(..., min_length=1, max_length=100, description="Magic system type")
    power_source: Optional[str] = Field(default=None, max_length=255, description="Power source")
    description: Optional[str] = Field(default=None, description="Description")
    mechanics: Optional[Dict[str, Any]] = Field(default=None, description="Mechanics")
    limitations: Optional[Dict[str, Any]] = Field(default=None, description="Limitations")


class MagicSystemCreate(MagicSystemBase):
    """Schema for creating a new magic system."""
    
    world_id: str = Field(..., description="World ID")


class MagicSystemUpdate(BaseSchema):
    """Schema for updating a magic system."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    type: Optional[str] = Field(default=None, min_length=1, max_length=100)
    power_source: Optional[str] = Field(default=None, max_length=255)
    world_id: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    mechanics: Optional[Dict[str, Any]] = Field(default=None)
    limitations: Optional[Dict[str, Any]] = Field(default=None)


class MagicSystemResponse(MagicSystemBase):
    """Schema for magic system response."""
    
    id: str
    world_id: str
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    has_mechanics: bool
    has_limitations: bool
    mechanics_list: List[str]
    limitations_list: List[str]
    
    # Related data (optional)
    world: Optional[Dict[str, Any]] = None


class MagicSystemList(BaseSchema):
    """Schema for magic system list response."""
    
    id: str
    name: str
    type: str
    world_id: str
    has_mechanics: bool
    has_limitations: bool
    created_at: datetime


class MagicSystemDetail(MagicSystemResponse):
    """Schema for detailed magic system response."""
    
    world: Dict[str, Any]


class MagicSystemFilters(BaseSchema):
    """Schema for magic system filters."""
    
    world_id: Optional[str] = Field(default=None, description="Filter by world")
    type: Optional[str] = Field(default=None, description="Filter by type")
    power_source: Optional[str] = Field(default=None, description="Filter by power source")
    search: Optional[str] = Field(default=None, description="Search by name")


# Paginated response types
MagicSystemPaginatedResponse = PaginatedResponse[MagicSystemList] 