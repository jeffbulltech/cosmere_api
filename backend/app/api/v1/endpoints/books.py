"""
Book API endpoints.
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_book_service, get_db
from app.services import BookService
from app.schemas.book import (
    BookCreate, BookUpdate, BookResponse, BookSummary, BookWithCharacters, 
    BookOverview, ReadingOrder
)
from app.schemas.base import PaginatedResponse, ErrorResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[BookResponse],
    summary="Get all books",
    description="Retrieve a paginated list of all books with optional filtering."
)
async def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of records to return"),
    title: Optional[str] = Query(None, description="Filter by book title"),
    series_id: Optional[str] = Query(None, description="Filter by series ID"),
    world_id: Optional[str] = Query(None, description="Filter by world ID"),
    is_standalone: Optional[bool] = Query(None, description="Filter by standalone status"),
    service: BookService = Depends(get_book_service)
):
    """Get all books with pagination and filtering."""
    filters = {}
    if title:
        filters["title"] = title
    if series_id:
        filters["series_id"] = series_id
    if world_id:
        filters["world_id"] = world_id
    if is_standalone is not None:
        filters["is_standalone"] = is_standalone
    
    books = service.get_multi(skip=skip, limit=limit, filters=filters, order_by="title")
    total = service.count(filters)
    
    return service.get_paginated_response(books, total, skip, limit)


@router.get(
    "/overview",
    response_model=BookOverview,
    summary="Get books overview",
    description="Get an overview of all books with statistics."
)
async def get_books_overview(
    service: BookService = Depends(get_book_service)
):
    """Get books overview with statistics."""
    return service.get_books_overview()


@router.get(
    "/standalone",
    response_model=List[BookResponse],
    summary="Get standalone books",
    description="Get all standalone books."
)
async def get_standalone_books(
    service: BookService = Depends(get_book_service)
):
    """Get standalone books."""
    return service.get_standalone_books()


@router.get(
    "/series/{series_id}",
    response_model=List[BookResponse],
    summary="Get books by series",
    description="Get all books in a specific series."
)
async def get_books_by_series(
    series_id: str,
    service: BookService = Depends(get_book_service)
):
    """Get books by series."""
    return service.get_books_by_series(series_id)


@router.get(
    "/world/{world_id}",
    response_model=List[BookResponse],
    summary="Get books by world",
    description="Get all books set in a specific world."
)
async def get_books_by_world(
    world_id: str,
    service: BookService = Depends(get_book_service)
):
    """Get books by world."""
    return service.get_books_by_world(world_id)


@router.get(
    "/reading-order/{series_id}",
    response_model=List[ReadingOrder],
    summary="Get reading order",
    description="Get the recommended reading order for a series."
)
async def get_reading_order(
    series_id: str,
    service: BookService = Depends(get_book_service)
):
    """Get reading order for a series."""
    return service.get_reading_order(series_id)


@router.get(
    "/search",
    response_model=List[BookResponse],
    summary="Search books",
    description="Search books by title and summary."
)
async def search_books(
    q: str = Query(..., min_length=1, description="Search term"),
    service: BookService = Depends(get_book_service)
):
    """Search books by title and summary."""
    return service.search_books(q)


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get book by ID",
    description="Get a specific book by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"}
    }
)
async def get_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    """Get a book by ID."""
    book = service.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get(
    "/{book_id}/characters",
    response_model=BookWithCharacters,
    summary="Get book with characters",
    description="Get a book with its character information.",
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"}
    }
)
async def get_book_with_characters(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    """Get book with characters."""
    book_data = service.get_book_with_characters(book_id)
    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_data


@router.get(
    "/{book_id}/summary",
    response_model=BookSummary,
    summary="Get book summary",
    description="Get a book with series and world information.",
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"}
    }
)
async def get_book_summary(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    """Get book summary with series and world info."""
    # This would need to be implemented in the service
    book = service.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # For now, return basic book info
    return {"book": book}


@router.get(
    "/title/{title}",
    response_model=BookResponse,
    summary="Get book by title",
    description="Get a book by its title.",
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"}
    }
)
async def get_book_by_title(
    title: str,
    service: BookService = Depends(get_book_service)
):
    """Get a book by title."""
    book = service.get_book_by_title(title)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post(
    "/",
    response_model=BookResponse,
    status_code=201,
    summary="Create book",
    description="Create a new book.",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        409: {"model": ErrorResponse, "description": "Book already exists"}
    }
)
async def create_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    """Create a new book."""
    # Check if book already exists
    if service.exists(book.id):
        raise HTTPException(status_code=409, detail="Book with this ID already exists")
    
    created_book = service.create(book.dict())
    if not created_book:
        raise HTTPException(status_code=400, detail="Failed to create book")
    
    return created_book


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update book",
    description="Update an existing book.",
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)
async def update_book(
    book_id: str,
    book_update: BookUpdate,
    service: BookService = Depends(get_book_service)
):
    """Update a book."""
    # Check if book exists
    if not service.exists(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = service.update(book_id, book_update.dict(exclude_unset=True))
    if not updated_book:
        raise HTTPException(status_code=400, detail="Failed to update book")
    
    return updated_book


@router.delete(
    "/{book_id}",
    status_code=204,
    summary="Delete book",
    description="Delete a book.",
    responses={
        404: {"model": ErrorResponse, "description": "Book not found"}
    }
)
async def delete_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
):
    """Delete a book."""
    if not service.exists(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    
    success = service.delete(book_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete book")
    
    return None
