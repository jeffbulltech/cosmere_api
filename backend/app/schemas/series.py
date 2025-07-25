"""
Series schemas for API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class SeriesBase(BaseSchema):
    """Base series schema with common fields."""
    
    name: str = Field(..., description="Series name", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Series description")
    world_id: Optional[str] = Field(None, description="World ID", max_length=50)
    planned_books: Optional[int] = Field(None, description="Number of planned books", ge=0)
    current_books: int = Field(0, description="Number of current books", ge=0)
    status: str = Field("ongoing", description="Series status")
    reading_order: Optional[str] = Field(None, description="Reading order information")


class SeriesCreate(SeriesBase):
    """Schema for creating a new series."""
    
    id: str = Field(..., description="Series ID", min_length=1, max_length=50)


class SeriesUpdate(BaseModel):
    """Schema for updating a series."""
    
    name: Optional[str] = Field(None, description="Series name", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Series description")
    world_id: Optional[str] = Field(None, description="World ID", max_length=50)
    planned_books: Optional[int] = Field(None, description="Number of planned books", ge=0)
    current_books: Optional[int] = Field(None, description="Number of current books", ge=0)
    status: Optional[str] = Field(None, description="Series status")
    reading_order: Optional[str] = Field(None, description="Reading order information")


class SeriesResponse(SeriesBase):
    """Schema for series response."""
    
    id: str = Field(..., description="Series ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class SeriesSummary(BaseSchema):
    """Schema for series summary with books."""
    
    series: SeriesResponse = Field(..., description="Series information")
    books: List[dict] = Field(..., description="Books in the series")
    world: Optional[dict] = Field(None, description="World information")
    total_books: int = Field(..., description="Total number of books")
    completed_books: int = Field(..., description="Number of completed books")


class SeriesOverview(BaseSchema):
    """Schema for series overview with statistics."""
    
    total_series: int = Field(..., description="Total number of series")
    ongoing_series: int = Field(..., description="Number of ongoing series")
    completed_series: int = Field(..., description="Number of completed series")
    series_by_world: dict = Field(..., description="Series grouped by world")
    average_completion_percentage: float = Field(..., description="Average completion percentage")
    series: List[SeriesResponse] = Field(..., description="List of series") 