"""
Character API endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_character_service, get_db
from app.services import CharacterService
from app.schemas.character import (
    CharacterCreate, CharacterUpdate, CharacterResponse, CharacterSummary, 
    CharacterNetwork, CharacterOverview
)
from app.schemas.base import PaginatedResponse, ErrorResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[CharacterResponse],
    summary="Get all characters",
    description="Retrieve a paginated list of all characters with optional filtering."
)
async def get_characters(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of records to return"),
    name: Optional[str] = Query(None, description="Filter by character name"),
    species: Optional[str] = Query(None, description="Filter by species"),
    status: Optional[str] = Query(None, description="Filter by character status"),
    world_id: Optional[str] = Query(None, description="Filter by world of origin"),
    service: CharacterService = Depends(get_character_service)
):
    """Get all characters with pagination and filtering."""
    filters = {}
    if name:
        filters["name"] = name
    if species:
        filters["species"] = species
    if status:
        filters["status"] = status
    if world_id:
        filters["world_of_origin_id"] = world_id
    
    characters = service.get_multi(skip=skip, limit=limit, filters=filters, order_by="name")
    total = service.count(filters)
    
    return service.get_paginated_response(characters, total, skip, limit)


@router.get(
    "/overview",
    response_model=CharacterOverview,
    summary="Get characters overview",
    description="Get an overview of all characters with statistics."
)
async def get_characters_overview(
    service: CharacterService = Depends(get_character_service)
):
    """Get characters overview with statistics."""
    return service.get_character_overview()


@router.get(
    "/world/{world_id}",
    response_model=List[CharacterResponse],
    summary="Get characters by world",
    description="Get all characters from a specific world."
)
async def get_characters_by_world(
    world_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get characters by world of origin."""
    return service.get_characters_by_world(world_id)


@router.get(
    "/species/{species}",
    response_model=List[CharacterResponse],
    summary="Get characters by species",
    description="Get all characters of a specific species."
)
async def get_characters_by_species(
    species: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get characters by species."""
    return service.get_characters_by_species(species)


@router.get(
    "/status/{status}",
    response_model=List[CharacterResponse],
    summary="Get characters by status",
    description="Get all characters with a specific status."
)
async def get_characters_by_status(
    status: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get characters by status."""
    return service.get_characters_by_status(status)


@router.get(
    "/magic-system/{magic_system_id}",
    response_model=List[CharacterResponse],
    summary="Get characters by magic system",
    description="Get all characters who use a specific magic system."
)
async def get_characters_by_magic_system(
    magic_system_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get characters by magic system."""
    return service.get_characters_by_magic_system(magic_system_id)


@router.get(
    "/book/{book_id}",
    response_model=List[CharacterResponse],
    summary="Get characters in book",
    description="Get all characters that appear in a specific book."
)
async def get_characters_in_book(
    book_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get characters in a book."""
    return service.get_characters_in_book(book_id)


@router.get(
    "/pov",
    response_model=List[CharacterResponse],
    summary="Get POV characters",
    description="Get all characters who have POV chapters."
)
async def get_pov_characters(
    service: CharacterService = Depends(get_character_service)
):
    """Get POV characters."""
    return service.get_pov_characters()


@router.get(
    "/search",
    response_model=List[CharacterResponse],
    summary="Search characters",
    description="Search characters by name, aliases, and biography."
)
async def search_characters(
    q: str = Query(..., min_length=1, description="Search term"),
    service: CharacterService = Depends(get_character_service)
):
    """Search characters by name, aliases, and biography."""
    return service.search_characters(q)


@router.get(
    "/{character_id}",
    response_model=CharacterResponse,
    summary="Get character by ID",
    description="Get a specific character by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Character not found"}
    }
)
async def get_character(
    character_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get a character by ID."""
    character = service.get(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.get(
    "/{character_id}/relationships",
    response_model=CharacterSummary,
    summary="Get character with relationships",
    description="Get a character with their relationship information.",
    responses={
        404: {"model": ErrorResponse, "description": "Character not found"}
    }
)
async def get_character_with_relationships(
    character_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get character with relationships."""
    character_data = service.get_character_with_relationships(character_id)
    if not character_data:
        raise HTTPException(status_code=404, detail="Character not found")
    return character_data


@router.get(
    "/{character_id}/network",
    response_model=CharacterNetwork,
    summary="Get character network",
    description="Get character relationship network data.",
    responses={
        404: {"model": ErrorResponse, "description": "Character not found"}
    }
)
async def get_character_network(
    character_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get character relationship network."""
    network_data = service.get_character_network(character_id)
    if not network_data:
        raise HTTPException(status_code=404, detail="Character not found")
    return network_data


@router.get(
    "/name/{name}",
    response_model=CharacterResponse,
    summary="Get character by name",
    description="Get a character by their name.",
    responses={
        404: {"model": ErrorResponse, "description": "Character not found"}
    }
)
async def get_character_by_name(
    name: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get a character by name."""
    character = service.get_character_by_name(name)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@router.get(
    "/alias/{alias}",
    response_model=List[CharacterResponse],
    summary="Get characters by alias",
    description="Get characters by one of their aliases."
)
async def get_characters_by_alias(
    alias: str,
    service: CharacterService = Depends(get_character_service)
):
    """Get characters by alias."""
    return service.get_characters_by_alias(alias)


@router.post(
    "/",
    response_model=CharacterResponse,
    status_code=201,
    summary="Create character",
    description="Create a new character.",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        409: {"model": ErrorResponse, "description": "Character already exists"}
    }
)
async def create_character(
    character: CharacterCreate,
    service: CharacterService = Depends(get_character_service)
):
    """Create a new character."""
    # Check if character already exists
    if service.exists(character.id):
        raise HTTPException(status_code=409, detail="Character with this ID already exists")
    
    created_character = service.create(character.dict())
    if not created_character:
        raise HTTPException(status_code=400, detail="Failed to create character")
    
    return created_character


@router.put(
    "/{character_id}",
    response_model=CharacterResponse,
    summary="Update character",
    description="Update an existing character.",
    responses={
        404: {"model": ErrorResponse, "description": "Character not found"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)
async def update_character(
    character_id: str,
    character_update: CharacterUpdate,
    service: CharacterService = Depends(get_character_service)
):
    """Update a character."""
    # Check if character exists
    if not service.exists(character_id):
        raise HTTPException(status_code=404, detail="Character not found")
    
    updated_character = service.update(character_id, character_update.dict(exclude_unset=True))
    if not updated_character:
        raise HTTPException(status_code=400, detail="Failed to update character")
    
    return updated_character


@router.delete(
    "/{character_id}",
    status_code=204,
    summary="Delete character",
    description="Delete a character.",
    responses={
        404: {"model": ErrorResponse, "description": "Character not found"}
    }
)
async def delete_character(
    character_id: str,
    service: CharacterService = Depends(get_character_service)
):
    """Delete a character."""
    if not service.exists(character_id):
        raise HTTPException(status_code=404, detail="Character not found")
    
    success = service.delete(character_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete character")
    
    return None
