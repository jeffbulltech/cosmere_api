from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from .base import BaseSchema, PaginatedResponse


class ShardBase(BaseSchema):
    """Base shard schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Shard name")
    intent: str = Field(..., min_length=1, max_length=255, description="Shard intent")
    vessel_name: Optional[str] = Field(default=None, max_length=255, description="Vessel name")
    vessel_status: Optional[str] = Field(default=None, max_length=100, description="Vessel status")
    description: Optional[str] = Field(default=None, description="Description")
    splinter_info: Optional[Dict[str, Any]] = Field(default=None, description="Splinter info")


class ShardCreate(ShardBase):
    """Schema for creating a new shard."""
    
    world_location_id: Optional[str] = Field(default=None, description="World location ID")


class ShardUpdate(BaseSchema):
    """Schema for updating a shard."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    intent: Optional[str] = Field(default=None, min_length=1, max_length=255)
    vessel_name: Optional[str] = Field(default=None, max_length=255)
    vessel_status: Optional[str] = Field(default=None, max_length=100)
    world_location_id: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    splinter_info: Optional[Dict[str, Any]] = Field(default=None)


class ShardResponse(ShardBase):
    """Schema for shard response."""
    
    id: str
    world_location_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    is_splintered: bool
    is_alive: bool
    has_world_location: bool
    world_count: int
    splinter_info_list: List[str]
    
    # Related data (optional)
    world_location: Optional[Dict[str, Any]] = None
    worlds: Optional[List[Dict[str, Any]]] = None


class ShardList(BaseSchema):
    """Schema for shard list response."""
    
    id: str
    name: str
    intent: str
    vessel_name: Optional[str] = None
    vessel_status: Optional[str] = None
    world_location_id: Optional[str] = None
    is_splintered: bool
    is_alive: bool
    has_world_location: bool
    world_count: int
    created_at: datetime


class ShardDetail(ShardResponse):
    """Schema for detailed shard response."""
    
    world_location: Optional[Dict[str, Any]] = None
    worlds: List[Dict[str, Any]]


class ShardFilters(BaseSchema):
    """Schema for shard filters."""
    
    intent: Optional[str] = Field(default=None, description="Filter by intent")
    vessel_status: Optional[str] = Field(default=None, description="Filter by vessel status")
    has_world_location: Optional[bool] = Field(default=None, description="Filter by world location")
    search: Optional[str] = Field(default=None, description="Search by name")


# Paginated response types
ShardPaginatedResponse = PaginatedResponse[ShardList] 