"""
Magic System schemas for API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class MagicSystemBase(BaseSchema):
    """Base magic system schema with common fields."""
    
    name: str = Field(..., description="Magic system name", min_length=1, max_length=100)
    world_id: Optional[str] = Field(None, description="World ID", max_length=50)
    description: Optional[str] = Field(None, description="Magic system description")
    mechanics: Optional[str] = Field(None, description="How the magic works")
    requirements: Optional[str] = Field(None, description="Requirements to use the magic")
    limitations: Optional[str] = Field(None, description="Limitations of the magic")
    is_investiture_based: bool = Field(True, description="Whether the magic is investiture-based")
    related_systems: Optional[str] = Field(None, description="Related magic systems")


class MagicSystemCreate(MagicSystemBase):
    """Schema for creating a new magic system."""
    
    id: str = Field(..., description="Magic system ID", min_length=1, max_length=50)


class MagicSystemUpdate(BaseModel):
    """Schema for updating a magic system."""
    
    name: Optional[str] = Field(None, description="Magic system name", min_length=1, max_length=100)
    world_id: Optional[str] = Field(None, description="World ID", max_length=50)
    description: Optional[str] = Field(None, description="Magic system description")
    mechanics: Optional[str] = Field(None, description="How the magic works")
    requirements: Optional[str] = Field(None, description="Requirements to use the magic")
    limitations: Optional[str] = Field(None, description="Limitations of the magic")
    is_investiture_based: Optional[bool] = Field(None, description="Whether the magic is investiture-based")
    related_systems: Optional[str] = Field(None, description="Related magic systems")


class MagicSystemResponse(MagicSystemBase):
    """Schema for magic system response."""
    
    id: str = Field(..., description="Magic system ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class MagicSystemSummary(BaseSchema):
    """Schema for magic system summary with users."""
    
    magic_system: MagicSystemResponse = Field(..., description="Magic system information")
    users: List[dict] = Field(..., description="Users of the magic system")
    active_users: List[dict] = Field(..., description="Active users of the magic system")
    world: Optional[dict] = Field(None, description="World information")


class MagicSystemOverview(BaseSchema):
    """Schema for magic system overview with statistics."""
    
    total_magic_systems: int = Field(..., description="Total number of magic systems")
    investiture_based: int = Field(..., description="Number of investiture-based systems")
    non_investiture_based: int = Field(..., description="Number of non-investiture-based systems")
    magic_systems_by_world: dict = Field(..., description="Magic systems grouped by world")
    total_users: int = Field(..., description="Total number of users")
    average_users_per_system: float = Field(..., description="Average users per system")
    magic_systems: List[MagicSystemResponse] = Field(..., description="List of magic systems") 