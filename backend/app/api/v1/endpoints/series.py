"""
Series API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_series_service, get_db
from app.services import SeriesService
from app.schemas.series import (
    SeriesCreate, SeriesUpdate, SeriesResponse, SeriesSummary, SeriesOverview
)
from app.schemas.base import PaginatedResponse, ErrorResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[SeriesResponse],
    summary="Get all series",
    description="Retrieve a paginated list of all series with optional filtering."
)
async def get_series(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of records to return"),
    name: Optional[str] = Query(None, description="Filter by series name"),
    status: Optional[str] = Query(None, description="Filter by series status"),
    world_id: Optional[str] = Query(None, description="Filter by world ID"),
    service: SeriesService = Depends(get_series_service)
):
    """Get all series with pagination and filtering."""
    filters = {}
    if name:
        filters["name"] = name
    if status:
        filters["status"] = status
    if world_id:
        filters["world_id"] = world_id
    
    series_list = service.get_multi(skip=skip, limit=limit, filters=filters, order_by="name")
    total = service.count(filters)
    
    return service.get_paginated_response(series_list, total, skip, limit)


@router.get(
    "/overview",
    response_model=SeriesOverview,
    summary="Get series overview",
    description="Get an overview of all series with statistics."
)
async def get_series_overview(
    service: SeriesService = Depends(get_series_service)
):
    """Get series overview with statistics."""
    return service.get_series_overview()


@router.get(
    "/ongoing",
    response_model=List[SeriesResponse],
    summary="Get ongoing series",
    description="Get all ongoing series."
)
async def get_ongoing_series(
    service: SeriesService = Depends(get_series_service)
):
    """Get ongoing series."""
    return service.get_ongoing_series()


@router.get(
    "/completed",
    response_model=List[SeriesResponse],
    summary="Get completed series",
    description="Get all completed series."
)
async def get_completed_series(
    service: SeriesService = Depends(get_series_service)
):
    """Get completed series."""
    return service.get_completed_series()


@router.get(
    "/world/{world_id}",
    response_model=List[SeriesResponse],
    summary="Get series by world",
    description="Get all series set in a specific world."
)
async def get_series_by_world(
    world_id: str,
    service: SeriesService = Depends(get_series_service)
):
    """Get series by world."""
    return service.get_series_by_world(world_id)


@router.get(
    "/status/{status}",
    response_model=List[SeriesResponse],
    summary="Get series by status",
    description="Get all series with a specific status."
)
async def get_series_by_status(
    status: str,
    service: SeriesService = Depends(get_series_service)
):
    """Get series by status."""
    return service.get_series_by_status(status)


@router.get(
    "/search",
    response_model=List[SeriesResponse],
    summary="Search series",
    description="Search series by name and description."
)
async def search_series(
    q: str = Query(..., min_length=1, description="Search term"),
    service: SeriesService = Depends(get_series_service)
):
    """Search series by name and description."""
    return service.search_series(q)


@router.get(
    "/{series_id}",
    response_model=SeriesResponse,
    summary="Get series by ID",
    description="Get a specific series by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Series not found"}
    }
)
async def get_series_by_id(
    series_id: str,
    service: SeriesService = Depends(get_series_service)
):
    """Get a series by ID."""
    series = service.get(series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series


@router.get(
    "/{series_id}/summary",
    response_model=SeriesSummary,
    summary="Get series summary",
    description="Get a series with its books and world information.",
    responses={
        404: {"model": ErrorResponse, "description": "Series not found"}
    }
)
async def get_series_summary(
    series_id: str,
    service: SeriesService = Depends(get_series_service)
):
    """Get series summary with books."""
    summary = service.get_series_summary(series_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Series not found")
    return summary


@router.get(
    "/name/{name}",
    response_model=SeriesResponse,
    summary="Get series by name",
    description="Get a series by its name.",
    responses={
        404: {"model": ErrorResponse, "description": "Series not found"}
    }
)
async def get_series_by_name(
    name: str,
    service: SeriesService = Depends(get_series_service)
):
    """Get a series by name."""
    series = service.get_series_by_name(name)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series


@router.post(
    "/",
    response_model=SeriesResponse,
    status_code=201,
    summary="Create series",
    description="Create a new series.",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        409: {"model": ErrorResponse, "description": "Series already exists"}
    }
)
async def create_series(
    series: SeriesCreate,
    service: SeriesService = Depends(get_series_service)
):
    """Create a new series."""
    # Check if series already exists
    if service.exists(series.id):
        raise HTTPException(status_code=409, detail="Series with this ID already exists")
    
    created_series = service.create(series.dict())
    if not created_series:
        raise HTTPException(status_code=400, detail="Failed to create series")
    
    return created_series


@router.put(
    "/{series_id}",
    response_model=SeriesResponse,
    summary="Update series",
    description="Update an existing series.",
    responses={
        404: {"model": ErrorResponse, "description": "Series not found"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)
async def update_series(
    series_id: str,
    series_update: SeriesUpdate,
    service: SeriesService = Depends(get_series_service)
):
    """Update a series."""
    # Check if series exists
    if not service.exists(series_id):
        raise HTTPException(status_code=404, detail="Series not found")
    
    updated_series = service.update(series_id, series_update.dict(exclude_unset=True))
    if not updated_series:
        raise HTTPException(status_code=400, detail="Failed to update series")
    
    return updated_series


@router.delete(
    "/{series_id}",
    status_code=204,
    summary="Delete series",
    description="Delete a series.",
    responses={
        404: {"model": ErrorResponse, "description": "Series not found"}
    }
)
async def delete_series(
    series_id: str,
    service: SeriesService = Depends(get_series_service)
):
    """Delete a series."""
    if not service.exists(series_id):
        raise HTTPException(status_code=404, detail="Series not found")
    
    success = service.delete(series_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete series")
    
    return None 