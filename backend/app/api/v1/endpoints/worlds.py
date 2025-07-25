"""
World API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_world_service, get_db
from app.services import WorldService
from app.schemas.world import (
    WorldCreate, WorldUpdate, WorldResponse, WorldSummary, WorldOverview
)
from app.schemas.base import PaginatedResponse, ErrorResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[WorldResponse],
    summary="Get all worlds",
    description="Retrieve a paginated list of all worlds with optional filtering."
)
async def get_worlds(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of records to return"),
    name: Optional[str] = Query(None, description="Filter by world name"),
    system: Optional[str] = Query(None, description="Filter by planetary system"),
    is_habitable: Optional[bool] = Query(None, description="Filter by habitable status"),
    service: WorldService = Depends(get_world_service)
):
    """Get all worlds with pagination and filtering."""
    filters = {}
    if name:
        filters["name"] = name
    if system:
        filters["system"] = system
    if is_habitable is not None:
        filters["is_habitable"] = is_habitable
    
    worlds = service.get_multi(skip=skip, limit=limit, filters=filters, order_by="name")
    total = service.count(filters)
    
    return service.get_paginated_response(worlds, total, skip, limit)


@router.get(
    "/overview",
    response_model=WorldOverview,
    summary="Get worlds overview",
    description="Get an overview of all worlds with statistics."
)
async def get_worlds_overview(
    service: WorldService = Depends(get_world_service)
):
    """Get worlds overview with statistics."""
    return service.get_worlds_overview()


@router.get(
    "/habitable",
    response_model=List[WorldResponse],
    summary="Get habitable worlds",
    description="Get all habitable worlds."
)
async def get_habitable_worlds(
    service: WorldService = Depends(get_world_service)
):
    """Get all habitable worlds."""
    return service.get_habitable_worlds()


@router.get(
    "/system/{system}",
    response_model=List[WorldResponse],
    summary="Get worlds by system",
    description="Get all worlds in a specific planetary system."
)
async def get_worlds_by_system(
    system: str,
    service: WorldService = Depends(get_world_service)
):
    """Get worlds by planetary system."""
    return service.get_worlds_by_system(system)


@router.get(
    "/with-series",
    response_model=List[WorldResponse],
    summary="Get worlds with series",
    description="Get worlds that have series associated with them."
)
async def get_worlds_with_series(
    service: WorldService = Depends(get_world_service)
):
    """Get worlds with series."""
    return service.get_worlds_with_series()


@router.get(
    "/with-magic-systems",
    response_model=List[WorldResponse],
    summary="Get worlds with magic systems",
    description="Get worlds that have magic systems."
)
async def get_worlds_with_magic_systems(
    service: WorldService = Depends(get_world_service)
):
    """Get worlds with magic systems."""
    return service.get_worlds_with_magic_systems()


@router.get(
    "/search",
    response_model=List[WorldResponse],
    summary="Search worlds",
    description="Search worlds by name and description."
)
async def search_worlds(
    q: str = Query(..., min_length=1, description="Search term"),
    service: WorldService = Depends(get_world_service)
):
    """Search worlds by name and description."""
    return service.search_worlds(q)


@router.get(
    "/{world_id}",
    response_model=WorldResponse,
    summary="Get world by ID",
    description="Get a specific world by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "World not found"}
    }
)
async def get_world(
    world_id: str,
    service: WorldService = Depends(get_world_service)
):
    """Get a world by ID."""
    world = service.get(world_id)
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    return world


@router.get(
    "/{world_id}/summary",
    response_model=WorldSummary,
    summary="Get world summary",
    description="Get a comprehensive summary of a world with statistics.",
    responses={
        404: {"model": ErrorResponse, "description": "World not found"}
    }
)
async def get_world_summary(
    world_id: str,
    service: WorldService = Depends(get_world_service)
):
    """Get world summary with statistics."""
    summary = service.get_world_summary(world_id)
    if not summary:
        raise HTTPException(status_code=404, detail="World not found")
    return summary


@router.get(
    "/name/{name}",
    response_model=WorldResponse,
    summary="Get world by name",
    description="Get a world by its name.",
    responses={
        404: {"model": ErrorResponse, "description": "World not found"}
    }
)
async def get_world_by_name(
    name: str,
    service: WorldService = Depends(get_world_service)
):
    """Get a world by name."""
    world = service.get_world_by_name(name)
    if not world:
        raise HTTPException(status_code=404, detail="World not found")
    return world


@router.post(
    "/",
    response_model=WorldResponse,
    status_code=201,
    summary="Create world",
    description="Create a new world.",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        409: {"model": ErrorResponse, "description": "World already exists"}
    }
)
async def create_world(
    world: WorldCreate,
    service: WorldService = Depends(get_world_service)
):
    """Create a new world."""
    # Check if world already exists
    if service.exists(world.id):
        raise HTTPException(status_code=409, detail="World with this ID already exists")
    
    created_world = service.create(world.dict())
    if not created_world:
        raise HTTPException(status_code=400, detail="Failed to create world")
    
    return created_world


@router.put(
    "/{world_id}",
    response_model=WorldResponse,
    summary="Update world",
    description="Update an existing world.",
    responses={
        404: {"model": ErrorResponse, "description": "World not found"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)
async def update_world(
    world_id: str,
    world_update: WorldUpdate,
    service: WorldService = Depends(get_world_service)
):
    """Update a world."""
    # Check if world exists
    if not service.exists(world_id):
        raise HTTPException(status_code=404, detail="World not found")
    
    updated_world = service.update(world_id, world_update.dict(exclude_unset=True))
    if not updated_world:
        raise HTTPException(status_code=400, detail="Failed to update world")
    
    return updated_world


@router.delete(
    "/{world_id}",
    status_code=204,
    summary="Delete world",
    description="Delete a world.",
    responses={
        404: {"model": ErrorResponse, "description": "World not found"}
    }
)
async def delete_world(
    world_id: str,
    service: WorldService = Depends(get_world_service)
):
    """Delete a world."""
    if not service.exists(world_id):
        raise HTTPException(status_code=404, detail="World not found")
    
    success = service.delete(world_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete world")
    
    return None
