from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.character import Character
from app.models.book import Book
from app.models.character_relationship import CharacterRelationship

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.get("/")
def list_characters(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    world_id: Optional[str] = None,
    status: Optional[str] = None,
    species: Optional[str] = None,
    magic_ability: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Character)
    if world_id:
        query = query.filter(Character.world_of_origin_id == world_id)
    if status:
        query = query.filter(Character.status == status)
    if species:
        query = query.filter(Character.species == species)
    if search:
        query = query.filter(Character.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    # Convert to simple dict format to avoid model method issues
    result = []
    for char in items:
        result.append({
            "id": char.id,
            "name": char.name,
            "world_of_origin_id": char.world_of_origin_id,
            "species": char.species,
            "status": char.status,
            "biography": char.biography,
            "created_at": char.created_at.isoformat() if char.created_at else None,
            "updated_at": char.updated_at.isoformat() if char.updated_at else None
        })
    
    return {
        "items": result,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_prev": skip > 0,
    }


@router.get("/{character_id}")
def get_character(character_id: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return {
        "id": character.id,
        "name": character.name,
        "world_of_origin_id": character.world_of_origin_id,
        "species": character.species,
        "status": character.status,
        "biography": character.biography,
        "created_at": character.created_at.isoformat() if character.created_at else None,
        "updated_at": character.updated_at.isoformat() if character.updated_at else None
    } 