from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.models.book import Book
from app.models.character import Character
from app.models.series import Series
from app.models.world import World
from app.schemas.book import (
    BookCreate, BookUpdate, BookResponse, BookList, BookPaginatedResponse, BookFilters
)
from app.schemas.character import CharacterList

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=BookPaginatedResponse)
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    series_id: Optional[str] = None,
    world_id: Optional[str] = None,
    publication_year: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Book)
    if series_id:
        query = query.filter(Book.series_id == series_id)
    if world_id:
        query = query.filter(Book.world_id == world_id)
    if publication_year:
        query = query.filter(Book.publication_date >= f"{publication_year}-01-01").filter(Book.publication_date < f"{publication_year + 1}-01-01")
    if search:
        query = query.filter(Book.title.ilike(f"%{search}%"))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {
        "items": [BookList.model_validate(b.to_dict()) for b in items],
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_prev": skip > 0,
    }


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    book = Book(**book_in.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return BookResponse.model_validate(book.to_dict())


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.model_validate(book.to_dict())


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: str, book_in: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in book_in.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return BookResponse.model_validate(book.to_dict())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return


@router.get("/series/{series_id}", response_model=List[BookList])
def get_books_by_series(series_id: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.series_id == series_id).all()
    return [BookList.model_validate(b.to_dict()) for b in books]


@router.get("/world/{world_id}", response_model=List[BookList])
def get_books_by_world(world_id: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.world_id == world_id).all()
    return [BookList.model_validate(b.to_dict()) for b in books]


@router.get("/{book_id}/characters", response_model=List[CharacterList])
def get_book_characters(book_id: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    characters = book.characters
    return [CharacterList.model_validate(c.to_dict()) for c in characters] 