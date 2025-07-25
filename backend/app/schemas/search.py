"""
Search schemas for API requests and responses.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class SearchRequest(BaseSchema):
    """Schema for search request."""
    
    search_term: str = Field(..., description="Search term", min_length=1)
    entity_types: Optional[List[str]] = Field(
        None, 
        description="Entity types to search in",
        example=["worlds", "books", "characters", "series", "magic_systems", "shards"]
    )
    filters: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional filters to apply"
    )
    limit: int = Field(50, description="Maximum number of results per entity type", ge=1, le=100)


class SearchResponse(BaseSchema):
    """Schema for search response."""
    
    search_term: str = Field(..., description="Search term used")
    total_results: int = Field(..., description="Total number of results")
    worlds: List[dict] = Field(..., description="World results")
    series: List[dict] = Field(..., description="Series results")
    books: List[dict] = Field(..., description="Book results")
    characters: List[dict] = Field(..., description="Character results")
    magic_systems: List[dict] = Field(..., description="Magic system results")
    shards: List[dict] = Field(..., description="Shard results")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filters applied")


class SearchSuggestion(BaseSchema):
    """Schema for search suggestion."""
    
    suggestions: List[str] = Field(..., description="List of search suggestions")
    search_term: str = Field(..., description="Original search term")


class AdvancedSearchRequest(BaseSchema):
    """Schema for advanced search request."""
    
    search_term: Optional[str] = Field(None, description="Search term")
    entity_types: Optional[List[str]] = Field(
        None, 
        description="Entity types to search in",
        example=["worlds", "books", "characters", "series", "magic_systems", "shards"]
    )
    filters: Optional[Dict[str, Any]] = Field(
        None, 
        description="Advanced filters to apply"
    )
    limit: int = Field(50, description="Maximum number of results per entity type", ge=1, le=100)
    order_by: Optional[str] = Field(None, description="Field to order results by")
    order_direction: str = Field("asc", description="Order direction (asc/desc)")


class SearchFilters(BaseSchema):
    """Schema for search filters."""
    
    # World filters
    is_habitable: Optional[bool] = Field(None, description="Filter by habitable worlds")
    system: Optional[str] = Field(None, description="Filter by planetary system")
    
    # Series filters
    status: Optional[str] = Field(None, description="Filter by series status")
    world_id: Optional[str] = Field(None, description="Filter by world")
    
    # Book filters
    is_standalone: Optional[bool] = Field(None, description="Filter by standalone books")
    series_id: Optional[str] = Field(None, description="Filter by series")
    
    # Character filters
    species: Optional[str] = Field(None, description="Filter by character species")
    character_status: Optional[str] = Field(None, description="Filter by character status")
    
    # Magic system filters
    is_investiture_based: Optional[bool] = Field(None, description="Filter by investiture-based magic")
    
    # Shard filters
    shard_status: Optional[str] = Field(None, description="Filter by shard status")
    is_combined: Optional[bool] = Field(None, description="Filter by combined shards") 