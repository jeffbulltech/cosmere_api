"""
Shard API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_shard_service, get_db
from app.services import ShardService
from app.schemas.shard import (
    ShardCreate, ShardUpdate, ShardResponse, ShardSummary, ShardOverview,
    ShardVesselCreate, ShardVesselResponse
)
from app.schemas.base import PaginatedResponse, ErrorResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[ShardResponse],
    summary="Get all shards",
    description="Retrieve a paginated list of all shards with optional filtering."
)
async def get_shards(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of records to return"),
    name: Optional[str] = Query(None, description="Filter by shard name"),
    intent: Optional[str] = Query(None, description="Filter by shard intent"),
    status: Optional[str] = Query(None, description="Filter by shard status"),
    is_combined: Optional[bool] = Query(None, description="Filter by combined status"),
    service: ShardService = Depends(get_shard_service)
):
    """Get all shards with pagination and filtering."""
    filters = {}
    if name:
        filters["name"] = name
    if intent:
        filters["intent"] = intent
    if status:
        filters["status"] = status
    if is_combined is not None:
        filters["is_combined"] = is_combined
    
    shards = service.get_multi(skip=skip, limit=limit, filters=filters, order_by="name")
    total = service.count(filters)
    
    return service.get_paginated_response(shards, total, skip, limit)


@router.get(
    "/overview",
    response_model=ShardOverview,
    summary="Get shards overview",
    description="Get an overview of all shards with statistics."
)
async def get_shards_overview(
    service: ShardService = Depends(get_shard_service)
):
    """Get shards overview with statistics."""
    return service.get_shards_overview()


@router.get(
    "/whole",
    response_model=List[ShardResponse],
    summary="Get whole shards",
    description="Get all whole shards."
)
async def get_whole_shards(
    service: ShardService = Depends(get_shard_service)
):
    """Get whole shards."""
    return service.get_whole_shards()


@router.get(
    "/splintered",
    response_model=List[ShardResponse],
    summary="Get splintered shards",
    description="Get all splintered shards."
)
async def get_splintered_shards(
    service: ShardService = Depends(get_shard_service)
):
    """Get splintered shards."""
    return service.get_splintered_shards()


@router.get(
    "/combined",
    response_model=List[ShardResponse],
    summary="Get combined shards",
    description="Get all combined shards."
)
async def get_combined_shards(
    service: ShardService = Depends(get_shard_service)
):
    """Get combined shards."""
    return service.get_combined_shards()


@router.get(
    "/intent/{intent}",
    response_model=List[ShardResponse],
    summary="Get shards by intent",
    description="Get all shards with a specific intent."
)
async def get_shards_by_intent(
    intent: str,
    service: ShardService = Depends(get_shard_service)
):
    """Get shards by intent."""
    return service.get_shards_by_intent(intent)


@router.get(
    "/status/{status}",
    response_model=List[ShardResponse],
    summary="Get shards by status",
    description="Get all shards with a specific status."
)
async def get_shards_by_status(
    status: str,
    service: ShardService = Depends(get_shard_service)
):
    """Get shards by status."""
    return service.get_shards_by_status(status)


@router.get(
    "/vessel/{vessel_name}",
    response_model=List[ShardResponse],
    summary="Get shards by vessel",
    description="Get all shards held by a specific vessel."
)
async def get_shards_by_vessel(
    vessel_name: str,
    service: ShardService = Depends(get_shard_service)
):
    """Get shards by vessel."""
    return service.get_shards_by_vessel(vessel_name)


@router.get(
    "/search",
    response_model=List[ShardResponse],
    summary="Search shards",
    description="Search shards by name, intent, and description."
)
async def search_shards(
    q: str = Query(..., min_length=1, description="Search term"),
    service: ShardService = Depends(get_shard_service)
):
    """Search shards by name, intent, and description."""
    return service.search_shards(q)


@router.get(
    "/{shard_id}",
    response_model=ShardResponse,
    summary="Get shard by ID",
    description="Get a specific shard by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Shard not found"}
    }
)
async def get_shard(
    shard_id: str,
    service: ShardService = Depends(get_shard_service)
):
    """Get a shard by ID."""
    shard = service.get(shard_id)
    if not shard:
        raise HTTPException(status_code=404, detail="Shard not found")
    return shard


@router.get(
    "/{shard_id}/vessels",
    response_model=ShardSummary,
    summary="Get shard with vessels",
    description="Get a shard with its vessel information.",
    responses={
        404: {"model": ErrorResponse, "description": "Shard not found"}
    }
)
async def get_shard_with_vessels(
    shard_id: str,
    service: ShardService = Depends(get_shard_service)
):
    """Get shard with vessels."""
    shard_data = service.get_shard_with_vessels(shard_id)
    if not shard_data:
        raise HTTPException(status_code=404, detail="Shard not found")
    return shard_data


@router.get(
    "/name/{name}",
    response_model=ShardResponse,
    summary="Get shard by name",
    description="Get a shard by its name.",
    responses={
        404: {"model": ErrorResponse, "description": "Shard not found"}
    }
)
async def get_shard_by_name(
    name: str,
    service: ShardService = Depends(get_shard_service)
):
    """Get a shard by name."""
    shard = service.get_shard_by_name(name)
    if not shard:
        raise HTTPException(status_code=404, detail="Shard not found")
    return shard


@router.post(
    "/",
    response_model=ShardResponse,
    status_code=201,
    summary="Create shard",
    description="Create a new shard.",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        409: {"model": ErrorResponse, "description": "Shard already exists"}
    }
)
async def create_shard(
    shard: ShardCreate,
    service: ShardService = Depends(get_shard_service)
):
    """Create a new shard."""
    # Check if shard already exists
    if service.exists(shard.id):
        raise HTTPException(status_code=409, detail="Shard with this ID already exists")
    
    created_shard = service.create(shard.dict())
    if not created_shard:
        raise HTTPException(status_code=400, detail="Failed to create shard")
    
    return created_shard


@router.put(
    "/{shard_id}",
    response_model=ShardResponse,
    summary="Update shard",
    description="Update an existing shard.",
    responses={
        404: {"model": ErrorResponse, "description": "Shard not found"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)
async def update_shard(
    shard_id: str,
    shard_update: ShardUpdate,
    service: ShardService = Depends(get_shard_service)
):
    """Update a shard."""
    # Check if shard exists
    if not service.exists(shard_id):
        raise HTTPException(status_code=404, detail="Shard not found")
    
    updated_shard = service.update(shard_id, shard_update.dict(exclude_unset=True))
    if not updated_shard:
        raise HTTPException(status_code=400, detail="Failed to update shard")
    
    return updated_shard


@router.delete(
    "/{shard_id}",
    status_code=204,
    summary="Delete shard",
    description="Delete a shard.",
    responses={
        404: {"model": ErrorResponse, "description": "Shard not found"}
    }
)
async def delete_shard(
    shard_id: str,
    service: ShardService = Depends(get_shard_service)
):
    """Delete a shard."""
    if not service.exists(shard_id):
        raise HTTPException(status_code=404, detail="Shard not found")
    
    success = service.delete(shard_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete shard")
    
    return None


# Shard Vessel endpoints
@router.post(
    "/{shard_id}/vessels",
    response_model=ShardVesselResponse,
    status_code=201,
    summary="Create shard vessel",
    description="Create a new vessel for a shard.",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        404: {"model": ErrorResponse, "description": "Shard not found"}
    }
)
async def create_shard_vessel(
    shard_id: str,
    vessel: ShardVesselCreate,
    service: ShardService = Depends(get_shard_service)
):
    """Create a new shard vessel."""
    # Check if shard exists
    if not service.exists(shard_id):
        raise HTTPException(status_code=404, detail="Shard not found")
    
    # This would need to be implemented in the service
    # For now, return a placeholder
    raise HTTPException(status_code=501, detail="Shard vessel creation not yet implemented") 