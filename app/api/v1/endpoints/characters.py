from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.character import Character
from app.models.book import Book
from app.models.character_relationship import CharacterRelationship
from app.schemas.character import (
    CharacterCreate, CharacterUpdate, CharacterResponse, CharacterList, CharacterPaginatedResponse, CharacterFilters
)
from app.schemas.book import BookList
from app.schemas.character_relationship import CharacterRelationshipResponse

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.get("/", response_model=CharacterPaginatedResponse)
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
    if magic_ability:
        query = query.filter(Character.magic_abilities.has_key(magic_ability))
    if search:
        query = query.filter(Character.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {
        "items": [CharacterList.model_validate(c.to_dict()) for c in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_prev": skip > 0,
    }


@router.post("/", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_character(character_in: CharacterCreate, db: Session = Depends(get_db)):
    character = Character(**character_in.model_dump())
    db.add(character)
    db.commit()
    db.refresh(character)
    return CharacterResponse.model_validate(character.to_dict())


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterResponse.model_validate(character.to_dict())


@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(character_id: str, character_in: CharacterUpdate, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    for field, value in character_in.model_dump(exclude_unset=True).items():
        setattr(character, field, value)
    db.commit()
    db.refresh(character)
    return CharacterResponse.model_validate(character.to_dict())


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(character)
    db.commit()
    return


@router.get("/{character_id}/relationships", response_model=List[CharacterRelationshipResponse])
def get_character_relationships(character_id: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    relationships = db.query(CharacterRelationship).filter(CharacterRelationship.character_id == character_id).all()
    return [CharacterRelationshipResponse.model_validate(r.to_dict()) for r in relationships]


@router.get("/{character_id}/appearances", response_model=List[BookList])
def get_character_appearances(character_id: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    books = character.books
    return [BookList.model_validate(b.to_dict()) for b in books] 