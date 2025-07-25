"""
Search API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_search_service, get_db
from app.services import SearchService
from app.schemas.search import (
    SearchRequest, SearchResponse, SearchSuggestion, AdvancedSearchRequest, SearchFilters
)
from app.schemas.base import ErrorResponse

router = APIRouter()


@router.get(
    "/",
    response_model=SearchResponse,
    summary="Search all entities",
    description="Search across all entity types with a single query."
)
async def search_all(
    q: str = Query(..., min_length=1, description="Search term"),
    limit_per_type: int = Query(10, ge=1, le=50, description="Maximum results per entity type"),
    service: SearchService = Depends(get_search_service)
):
    """Search across all entity types."""
    return service.search_all(q, limit_per_type)


@router.get(
    "/suggestions",
    response_model=SearchSuggestion,
    summary="Get search suggestions",
    description="Get search suggestions based on partial input."
)
async def get_search_suggestions(
    q: str = Query(..., min_length=1, description="Partial search term"),
    limit: int = Query(10, ge=1, le=20, description="Maximum number of suggestions"),
    service: SearchService = Depends(get_search_service)
):
    """Get search suggestions."""
    suggestions = service.get_search_suggestions(q, limit)
    return SearchSuggestion(suggestions=suggestions, search_term=q)


@router.get(
    "/{entity_type}",
    response_model=List[dict],
    summary="Search by entity type",
    description="Search within a specific entity type."
)
async def search_by_type(
    entity_type: str,
    q: str = Query(..., min_length=1, description="Search term"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    service: SearchService = Depends(get_search_service)
):
    """Search within a specific entity type."""
    valid_types = ["worlds", "series", "books", "characters", "magic_systems", "shards"]
    if entity_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid entity type. Must be one of: {valid_types}")
    
    return service.search_by_type(q, entity_type, limit)


@router.post(
    "/advanced",
    response_model=SearchResponse,
    summary="Advanced search",
    description="Advanced search with filters and entity type selection."
)
async def advanced_search(
    search_request: AdvancedSearchRequest,
    service: SearchService = Depends(get_search_service)
):
    """Advanced search with filters."""
    return service.advanced_search(
        search_term=search_request.search_term,
        entity_types=search_request.entity_types,
        filters=search_request.filters,
        limit=search_request.limit
    )


@router.get(
    "/worlds",
    response_model=List[dict],
    summary="Search worlds",
    description="Search worlds with filters."
)
async def search_worlds(
    q: str = Query(..., min_length=1, description="Search term"),
    is_habitable: Optional[bool] = Query(None, description="Filter by habitable status"),
    system: Optional[str] = Query(None, description="Filter by planetary system"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    service: SearchService = Depends(get_search_service)
):
    """Search worlds with filters."""
    filters = {}
    if is_habitable is not None:
        filters["is_habitable"] = is_habitable
    if system:
        filters["system"] = system
    
    return service.advanced_search(
        search_term=q,
        entity_types=["worlds"],
        filters=filters,
        limit=limit
    )["worlds"]


@router.get(
    "/books",
    response_model=List[dict],
    summary="Search books",
    description="Search books with filters."
)
async def search_books(
    q: str = Query(..., min_length=1, description="Search term"),
    is_standalone: Optional[bool] = Query(None, description="Filter by standalone status"),
    world_id: Optional[str] = Query(None, description="Filter by world ID"),
    series_id: Optional[str] = Query(None, description="Filter by series ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    service: SearchService = Depends(get_search_service)
):
    """Search books with filters."""
    filters = {}
    if is_standalone is not None:
        filters["is_standalone"] = is_standalone
    if world_id:
        filters["world_id"] = world_id
    if series_id:
        filters["series_id"] = series_id
    
    return service.advanced_search(
        search_term=q,
        entity_types=["books"],
        filters=filters,
        limit=limit
    )["books"]


@router.get(
    "/characters",
    response_model=List[dict],
    summary="Search characters",
    description="Search characters with filters."
)
async def search_characters(
    q: str = Query(..., min_length=1, description="Search term"),
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by character status"),
    world_id: Optional[str] = Query(None, description="Filter by world ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    service: SearchService = Depends(get_search_service)
):
    """Search characters with filters."""
    filters = {}
    if species:
        filters["species"] = species
    if status:
        filters["status"] = status
    if world_id:
        filters["world_id"] = world_id
    
    return service.advanced_search(
        search_term=q,
        entity_types=["characters"],
        filters=filters,
        limit=limit
    )["characters"]


@router.get(
    "/series",
    response_model=List[dict],
    summary="Search series",
    description="Search series with filters."
)
async def search_series(
    q: str = Query(..., min_length=1, description="Search term"),
    status: Optional[str] = Query(None, description="Filter by series status"),
    world_id: Optional[str] = Query(None, description="Filter by world ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    service: SearchService = Depends(get_search_service)
):
    """Search series with filters."""
    filters = {}
    if status:
        filters["status"] = status
    if world_id:
        filters["world_id"] = world_id
    
    return service.advanced_search(
        search_term=q,
        entity_types=["series"],
        filters=filters,
        limit=limit
    )["series"]


@router.get(
    "/magic-systems",
    response_model=List[dict],
    summary="Search magic systems",
    description="Search magic systems with filters."
)
async def search_magic_systems(
    q: str = Query(..., min_length=1, description="Search term"),
    is_investiture_based: Optional[bool] = Query(None, description="Filter by investiture-based status"),
    world_id: Optional[str] = Query(None, description="Filter by world ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    service: SearchService = Depends(get_search_service)
):
    """Search magic systems with filters."""
    filters = {}
    if is_investiture_based is not None:
        filters["is_investiture_based"] = is_investiture_based
    if world_id:
        filters["world_id"] = world_id
    
    return service.advanced_search(
        search_term=q,
        entity_types=["magic_systems"],
        filters=filters,
        limit=limit
    )["magic_systems"]


@router.get(
    "/shards",
    response_model=List[dict],
    summary="Search shards",
    description="Search shards with filters."
)
async def search_shards(
    q: str = Query(..., min_length=1, description="Search term"),
    status: Optional[str] = Query(None, description="Filter by shard status"),
    is_combined: Optional[bool] = Query(None, description="Filter by combined status"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    service: SearchService = Depends(get_search_service)
):
    """Search shards with filters."""
    filters = {}
    if status:
        filters["status"] = status
    if is_combined is not None:
        filters["is_combined"] = is_combined
    
    return service.advanced_search(
        search_term=q,
        entity_types=["shards"],
        filters=filters,
        limit=limit
    )["shards"] 