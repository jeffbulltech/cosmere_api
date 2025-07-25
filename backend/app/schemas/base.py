"""
Base schemas for common API patterns.
"""
from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated response schema."""
    
    items: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Number of items per page")
    page: int = Field(..., description="Current page number")
    pages: int = Field(..., description="Total number of pages")


class ErrorResponse(BaseSchema):
    """Error response schema."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")


class SuccessResponse(BaseSchema):
    """Success response schema."""
    
    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Response data")


class HealthResponse(BaseSchema):
    """Health check response schema."""
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    version: Optional[str] = Field(None, description="API version") 