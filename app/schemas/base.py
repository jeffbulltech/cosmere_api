from pydantic import BaseModel, Field, ConfigDict
from typing import Generic, TypeVar, List, Optional, Any
from datetime import datetime
import uuid

# Generic type for paginated responses
T = TypeVar('T')


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v)
        }
    )


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response schema."""
    
    items: List[T]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


class SearchResult(BaseSchema, Generic[T]):
    """Generic search result schema."""
    
    items: List[T]
    total: int
    query: str
    took: float
    has_next: bool
    has_prev: bool


class ErrorResponse(BaseSchema):
    """Error response schema."""
    
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class SuccessResponse(BaseSchema):
    """Success response schema."""
    
    message: str
    data: Optional[Any] = None


class HealthCheck(BaseSchema):
    """Health check response schema."""
    
    status: str
    timestamp: datetime
    version: str
    database: Optional[dict] = None
    redis: Optional[dict] = None
    elasticsearch: Optional[dict] = None


class PaginationParams(BaseSchema):
    """Pagination parameters for API endpoints."""
    
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Number of items to return")
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$", description="Sort order")


class SearchParams(BaseSchema):
    """Search parameters for API endpoints."""
    
    q: str = Field(..., min_length=1, description="Search query")
    size: int = Field(default=20, ge=1, le=100, description="Number of results to return")
    filters: Optional[dict] = Field(default=None, description="Additional filters")


class FilterParams(BaseSchema):
    """Common filter parameters."""
    
    world_id: Optional[str] = Field(default=None, description="Filter by world ID")
    series_id: Optional[str] = Field(default=None, description="Filter by series ID")
    status: Optional[str] = Field(default=None, description="Filter by status")
    species: Optional[str] = Field(default=None, description="Filter by species")
    magic_ability: Optional[str] = Field(default=None, description="Filter by magic ability")
    relationship_type: Optional[str] = Field(default=None, description="Filter by relationship type")


class ApiResponse(BaseSchema, Generic[T]):
    """Standard API response wrapper."""
    
    data: T
    meta: dict = Field(default_factory=dict)
    links: Optional[dict] = Field(default=None)


class BulkResponse(BaseSchema, Generic[T]):
    """Bulk operation response schema."""
    
    created: List[T]
    updated: List[T]
    deleted: List[str]
    errors: List[dict] = Field(default_factory=list)
    total_processed: int
    success_count: int
    error_count: int 