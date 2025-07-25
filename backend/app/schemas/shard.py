"""
Shard schemas for API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class ShardBase(BaseSchema):
    """Base shard schema with common fields."""
    
    name: str = Field(..., description="Shard name", min_length=1, max_length=100)
    intent: Optional[str] = Field(None, description="Shard intent", max_length=100)
    status: str = Field("unknown", description="Shard status")
    current_vessel: Optional[str] = Field(None, description="Current vessel name", max_length=100)
    original_vessel: Optional[str] = Field(None, description="Original vessel name", max_length=100)
    description: Optional[str] = Field(None, description="Shard description")
    perpendicularity: Optional[str] = Field(None, description="Perpendicularity location")
    magic_systems: Optional[str] = Field(None, description="Associated magic systems")
    residence: Optional[str] = Field(None, description="Shard residence")
    is_combined: bool = Field(False, description="Whether the shard is combined")


class ShardCreate(ShardBase):
    """Schema for creating a new shard."""
    
    id: str = Field(..., description="Shard ID", min_length=1, max_length=50)


class ShardUpdate(BaseModel):
    """Schema for updating a shard."""
    
    name: Optional[str] = Field(None, description="Shard name", min_length=1, max_length=100)
    intent: Optional[str] = Field(None, description="Shard intent", max_length=100)
    status: Optional[str] = Field(None, description="Shard status")
    current_vessel: Optional[str] = Field(None, description="Current vessel name", max_length=100)
    original_vessel: Optional[str] = Field(None, description="Original vessel name", max_length=100)
    description: Optional[str] = Field(None, description="Shard description")
    perpendicularity: Optional[str] = Field(None, description="Perpendicularity location")
    magic_systems: Optional[str] = Field(None, description="Associated magic systems")
    residence: Optional[str] = Field(None, description="Shard residence")
    is_combined: Optional[bool] = Field(None, description="Whether the shard is combined")


class ShardResponse(ShardBase):
    """Schema for shard response."""
    
    id: str = Field(..., description="Shard ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ShardVesselBase(BaseSchema):
    """Base shard vessel schema with common fields."""
    
    shard_id: str = Field(..., description="Shard ID", max_length=50)
    vessel_name: str = Field(..., description="Vessel name", min_length=1, max_length=100)
    vessel_type: str = Field(..., description="Vessel type (original, current, etc.)")
    start_date: Optional[str] = Field(None, description="Start date as vessel")
    end_date: Optional[str] = Field(None, description="End date as vessel")
    description: Optional[str] = Field(None, description="Vessel description")


class ShardVesselCreate(ShardVesselBase):
    """Schema for creating a new shard vessel."""
    
    id: str = Field(..., description="Vessel ID", min_length=1, max_length=50)


class ShardVesselResponse(ShardVesselBase):
    """Schema for shard vessel response."""
    
    id: str = Field(..., description="Vessel ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ShardSummary(BaseSchema):
    """Schema for shard summary with vessels."""
    
    shard: ShardResponse = Field(..., description="Shard information")
    vessels: List[ShardVesselResponse] = Field(..., description="Shard vessels")
    current_vessel: Optional[ShardVesselResponse] = Field(None, description="Current vessel")
    original_vessel: Optional[ShardVesselResponse] = Field(None, description="Original vessel")


class ShardOverview(BaseSchema):
    """Schema for shard overview with statistics."""
    
    total_shards: int = Field(..., description="Total number of shards")
    whole_shards: int = Field(..., description="Number of whole shards")
    splintered_shards: int = Field(..., description="Number of splintered shards")
    combined_shards: int = Field(..., description="Number of combined shards")
    shards_by_status: dict = Field(..., description="Shards grouped by status")
    total_vessels: int = Field(..., description="Total number of vessels")
    average_vessels_per_shard: float = Field(..., description="Average vessels per shard")
    shards: List[ShardResponse] = Field(..., description="List of shards") 