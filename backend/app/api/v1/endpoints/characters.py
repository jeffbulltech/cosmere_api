from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.models.character import Character

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_characters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all characters with pagination"""
    characters = db.query(Character).offset(skip).limit(limit).all()
    # Convert to simple dict format to avoid model method issues
    result = []
    for char in characters:
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
    return {"items": result, "total": len(result), "skip": skip, "limit": limit}

@router.get("/{character_id}")
def get_character(character_id: str, db: Session = Depends(get_db)):
    """Get a specific character by ID"""
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
