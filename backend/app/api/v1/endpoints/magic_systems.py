"""
Magic System API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_magic_system_service, get_db
from app.services import MagicSystemService
from app.schemas.magic_system import (
    MagicSystemCreate, MagicSystemUpdate, MagicSystemResponse, 
    MagicSystemSummary, MagicSystemOverview
)
from app.schemas.base import PaginatedResponse, ErrorResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[MagicSystemResponse],
    summary="Get all magic systems",
    description="Retrieve a paginated list of all magic systems with optional filtering."
)
async def get_magic_systems(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of records to return"),
    name: Optional[str] = Query(None, description="Filter by magic system name"),
    world_id: Optional[str] = Query(None, description="Filter by world ID"),
    is_investiture_based: Optional[bool] = Query(None, description="Filter by investiture-based status"),
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get all magic systems with pagination and filtering."""
    filters = {}
    if name:
        filters["name"] = name
    if world_id:
        filters["world_id"] = world_id
    if is_investiture_based is not None:
        filters["is_investiture_based"] = is_investiture_based
    
    magic_systems = service.get_multi(skip=skip, limit=limit, filters=filters, order_by="name")
    total = service.count(filters)
    
    return service.get_paginated_response(magic_systems, total, skip, limit)


@router.get(
    "/overview",
    response_model=MagicSystemOverview,
    summary="Get magic systems overview",
    description="Get an overview of all magic systems with statistics."
)
async def get_magic_systems_overview(
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get magic systems overview with statistics."""
    return service.get_magic_systems_overview()


@router.get(
    "/investiture-based",
    response_model=List[MagicSystemResponse],
    summary="Get investiture-based magic systems",
    description="Get all investiture-based magic systems."
)
async def get_investiture_based_magic_systems(
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get investiture-based magic systems."""
    return service.get_investiture_based()


@router.get(
    "/world/{world_id}",
    response_model=List[MagicSystemResponse],
    summary="Get magic systems by world",
    description="Get all magic systems from a specific world."
)
async def get_magic_systems_by_world(
    world_id: str,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get magic systems by world."""
    return service.get_magic_systems_by_world(world_id)


@router.get(
    "/world/{world_id}/with-stats",
    response_model=List[dict],
    summary="Get magic systems by world with statistics",
    description="Get magic systems from a specific world with user statistics."
)
async def get_magic_systems_by_world_with_stats(
    world_id: str,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get magic systems by world with statistics."""
    return service.get_magic_systems_by_world_with_stats(world_id)


@router.get(
    "/search",
    response_model=List[MagicSystemResponse],
    summary="Search magic systems",
    description="Search magic systems by name and description."
)
async def search_magic_systems(
    q: str = Query(..., min_length=1, description="Search term"),
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Search magic systems by name and description."""
    return service.search_magic_systems(q)


@router.get(
    "/{magic_system_id}",
    response_model=MagicSystemResponse,
    summary="Get magic system by ID",
    description="Get a specific magic system by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Magic system not found"}
    }
)
async def get_magic_system(
    magic_system_id: str,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get a magic system by ID."""
    magic_system = service.get(magic_system_id)
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    return magic_system


@router.get(
    "/{magic_system_id}/users",
    response_model=MagicSystemSummary,
    summary="Get magic system with users",
    description="Get a magic system with its users information.",
    responses={
        404: {"model": ErrorResponse, "description": "Magic system not found"}
    }
)
async def get_magic_system_with_users(
    magic_system_id: str,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get magic system with users."""
    magic_system_data = service.get_magic_system_with_users(magic_system_id)
    if not magic_system_data:
        raise HTTPException(status_code=404, detail="Magic system not found")
    return magic_system_data


@router.get(
    "/name/{name}",
    response_model=MagicSystemResponse,
    summary="Get magic system by name",
    description="Get a magic system by its name.",
    responses={
        404: {"model": ErrorResponse, "description": "Magic system not found"}
    }
)
async def get_magic_system_by_name(
    name: str,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Get a magic system by name."""
    magic_system = service.get_magic_system_by_name(name)
    if not magic_system:
        raise HTTPException(status_code=404, detail="Magic system not found")
    return magic_system


@router.post(
    "/",
    response_model=MagicSystemResponse,
    status_code=201,
    summary="Create magic system",
    description="Create a new magic system.",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        409: {"model": ErrorResponse, "description": "Magic system already exists"}
    }
)
async def create_magic_system(
    magic_system: MagicSystemCreate,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Create a new magic system."""
    # Check if magic system already exists
    if service.exists(magic_system.id):
        raise HTTPException(status_code=409, detail="Magic system with this ID already exists")
    
    created_magic_system = service.create(magic_system.dict())
    if not created_magic_system:
        raise HTTPException(status_code=400, detail="Failed to create magic system")
    
    return created_magic_system


@router.put(
    "/{magic_system_id}",
    response_model=MagicSystemResponse,
    summary="Update magic system",
    description="Update an existing magic system.",
    responses={
        404: {"model": ErrorResponse, "description": "Magic system not found"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)
async def update_magic_system(
    magic_system_id: str,
    magic_system_update: MagicSystemUpdate,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Update a magic system."""
    # Check if magic system exists
    if not service.exists(magic_system_id):
        raise HTTPException(status_code=404, detail="Magic system not found")
    
    updated_magic_system = service.update(magic_system_id, magic_system_update.dict(exclude_unset=True))
    if not updated_magic_system:
        raise HTTPException(status_code=400, detail="Failed to update magic system")
    
    return updated_magic_system


@router.delete(
    "/{magic_system_id}",
    status_code=204,
    summary="Delete magic system",
    description="Delete a magic system.",
    responses={
        404: {"model": ErrorResponse, "description": "Magic system not found"}
    }
)
async def delete_magic_system(
    magic_system_id: str,
    service: MagicSystemService = Depends(get_magic_system_service)
):
    """Delete a magic system."""
    if not service.exists(magic_system_id):
        raise HTTPException(status_code=404, detail="Magic system not found")
    
    success = service.delete(magic_system_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete magic system")
    
    return None
