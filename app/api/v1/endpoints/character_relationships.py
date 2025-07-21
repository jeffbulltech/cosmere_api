from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.character_relationship import CharacterRelationship
from app.models.character import Character
from app.models.book import Book
from app.schemas.character_relationship import (
    CharacterRelationshipCreate, CharacterRelationshipUpdate, CharacterRelationshipResponse
)
from app.schemas.character import CharacterList
from app.schemas.book import BookList

router = APIRouter(prefix="/character-relationships", tags=["Character Relationships"])


@router.get("/", response_model=List[CharacterRelationshipResponse])
def list_character_relationships(
    character_id: Optional[str] = None,
    related_character_id: Optional[str] = None,
    relationship_type: Optional[str] = None,
    book_context_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(CharacterRelationship)
    if character_id:
        query = query.filter(CharacterRelationship.character_id == character_id)
    if related_character_id:
        query = query.filter(CharacterRelationship.related_character_id == related_character_id)
    if relationship_type:
        query = query.filter(CharacterRelationship.relationship_type == relationship_type)
    if book_context_id:
        query = query.filter(CharacterRelationship.book_context_id == book_context_id)
    items = query.all()
    return [CharacterRelationshipResponse.model_validate(r.to_dict()) for r in items]


@router.post("/", response_model=CharacterRelationshipResponse, status_code=status.HTTP_201_CREATED)
def create_character_relationship(relationship_in: CharacterRelationshipCreate, db: Session = Depends(get_db)):
    relationship = CharacterRelationship(**relationship_in.model_dump())
    db.add(relationship)
    db.commit()
    db.refresh(relationship)
    return CharacterRelationshipResponse.model_validate(relationship.to_dict())


@router.get("/{relationship_id}", response_model=CharacterRelationshipResponse)
def get_character_relationship(relationship_id: str, db: Session = Depends(get_db)):
    relationship = db.query(CharacterRelationship).filter(CharacterRelationship.id == relationship_id).first()
    if not relationship:
        raise HTTPException(status_code=404, detail="Character relationship not found")
    return CharacterRelationshipResponse.model_validate(relationship.to_dict())


@router.put("/{relationship_id}", response_model=CharacterRelationshipResponse)
def update_character_relationship(relationship_id: str, relationship_in: CharacterRelationshipUpdate, db: Session = Depends(get_db)):
    relationship = db.query(CharacterRelationship).filter(CharacterRelationship.id == relationship_id).first()
    if not relationship:
        raise HTTPException(status_code=404, detail="Character relationship not found")
    for field, value in relationship_in.model_dump(exclude_unset=True).items():
        setattr(relationship, field, value)
    db.commit()
    db.refresh(relationship)
    return CharacterRelationshipResponse.model_validate(relationship.to_dict())


@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character_relationship(relationship_id: str, db: Session = Depends(get_db)):
    relationship = db.query(CharacterRelationship).filter(CharacterRelationship.id == relationship_id).first()
    if not relationship:
        raise HTTPException(status_code=404, detail="Character relationship not found")
    db.delete(relationship)
    db.commit()
    return


@router.get("/{relationship_id}/character", response_model=CharacterList)
def get_relationship_character(relationship_id: str, db: Session = Depends(get_db)):
    relationship = db.query(CharacterRelationship).filter(CharacterRelationship.id == relationship_id).first()
    if not relationship:
        raise HTTPException(status_code=404, detail="Character relationship not found")
    character = db.query(Character).filter(Character.id == relationship.character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return CharacterList.model_validate(character.to_dict())


@router.get("/{relationship_id}/related-character", response_model=CharacterList)
def get_relationship_related_character(relationship_id: str, db: Session = Depends(get_db)):
    relationship = db.query(CharacterRelationship).filter(CharacterRelationship.id == relationship_id).first()
    if not relationship:
        raise HTTPException(status_code=404, detail="Character relationship not found")
    character = db.query(Character).filter(Character.id == relationship.related_character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Related character not found")
    return CharacterList.model_validate(character.to_dict())


@router.get("/{relationship_id}/book-context", response_model=BookList)
def get_relationship_book_context(relationship_id: str, db: Session = Depends(get_db)):
    relationship = db.query(CharacterRelationship).filter(CharacterRelationship.id == relationship_id).first()
    if not relationship:
        raise HTTPException(status_code=404, detail="Character relationship not found")
    if not relationship.book_context_id:
        raise HTTPException(status_code=404, detail="Relationship does not have a book context")
    book = db.query(Book).filter(Book.id == relationship.book_context_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookList.model_validate(book.to_dict()) 