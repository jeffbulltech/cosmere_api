"""
World schemas for API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class WorldBase(BaseSchema):
    """Base world schema with common fields."""
    
    name: str = Field(..., description="World name", min_length=1, max_length=255)
    system: Optional[str] = Field(None, description="Planetary system", max_length=255)
    shard_id: Optional[str] = Field(None, description="Shard ID", max_length=36)
    geography: Optional[str] = Field(None, description="Geography information (JSON)")
    culture_notes: Optional[str] = Field(None, description="Cultural notes")
    technology_level: Optional[str] = Field(None, description="Technology level", max_length=100)


class WorldCreate(WorldBase):
    """Schema for creating a new world."""
    
    id: str = Field(..., description="World ID", min_length=1, max_length=50)


class WorldUpdate(BaseModel):
    """Schema for updating a world."""
    
    name: Optional[str] = Field(None, description="World name", min_length=1, max_length=255)
    system: Optional[str] = Field(None, description="Planetary system", max_length=255)
    shard_id: Optional[str] = Field(None, description="Shard ID", max_length=36)
    geography: Optional[str] = Field(None, description="Geography information (JSON)")
    culture_notes: Optional[str] = Field(None, description="Cultural notes")
    technology_level: Optional[str] = Field(None, description="Technology level", max_length=100)


class WorldResponse(WorldBase):
    """Schema for world response."""
    
    id: str = Field(..., description="World ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class WorldSummary(BaseSchema):
    """Schema for world summary with statistics."""
    
    world: WorldResponse = Field(..., description="World information")
    series_count: int = Field(..., description="Number of series")
    books_count: int = Field(..., description="Number of books")
    characters_count: int = Field(..., description="Number of characters")
    magic_systems_count: int = Field(..., description="Number of magic systems")
    series_completion_percentage: float = Field(..., description="Series completion percentage")
    has_magic_systems: bool = Field(..., description="Whether the world has magic systems")
    has_characters: bool = Field(..., description="Whether the world has characters")


class WorldOverview(BaseSchema):
    """Schema for world overview with statistics."""
    
    total_worlds: int = Field(..., description="Total number of worlds")
    habitable_worlds: int = Field(..., description="Number of habitable worlds")
    worlds_with_series: int = Field(..., description="Number of worlds with series")
    worlds_with_magic_systems: int = Field(..., description="Number of worlds with magic systems")
    worlds: List[WorldResponse] = Field(..., description="List of worlds") 