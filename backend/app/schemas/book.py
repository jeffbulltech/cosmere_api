"""
Book schemas for API requests and responses.
"""
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class BookBase(BaseSchema):
    """Base book schema with common fields."""
    
    title: str = Field(..., description="Book title", min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, description="ISBN", max_length=20)
    publication_date: Optional[date] = Field(None, description="Publication date")
    word_count: Optional[int] = Field(None, description="Word count", ge=0)
    chronological_order: Optional[int] = Field(None, description="Chronological order", ge=0)
    series_id: Optional[str] = Field(None, description="Series ID", max_length=36)
    world_id: str = Field(..., description="World ID", max_length=36)
    summary: Optional[str] = Field(None, description="Book summary")
    cosmere_significance: Optional[str] = Field(None, description="Cosmere significance")


class BookCreate(BookBase):
    """Schema for creating a new book."""
    
    id: str = Field(..., description="Book ID", min_length=1, max_length=50)


class BookUpdate(BaseModel):
    """Schema for updating a book."""
    
    title: Optional[str] = Field(None, description="Book title", min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, description="ISBN", max_length=20)
    publication_date: Optional[date] = Field(None, description="Publication date")
    word_count: Optional[int] = Field(None, description="Word count", ge=0)
    chronological_order: Optional[int] = Field(None, description="Chronological order", ge=0)
    series_id: Optional[str] = Field(None, description="Series ID", max_length=36)
    world_id: Optional[str] = Field(None, description="World ID", max_length=36)
    summary: Optional[str] = Field(None, description="Book summary")
    cosmere_significance: Optional[str] = Field(None, description="Cosmere significance")


class BookResponse(BookBase):
    """Schema for book response."""
    
    id: str = Field(..., description="Book ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class BookSummary(BaseSchema):
    """Schema for book summary with series and world info."""
    
    book: BookResponse = Field(..., description="Book information")
    series: Optional[dict] = Field(None, description="Series information")
    world: Optional[dict] = Field(None, description="World information")


class BookWithCharacters(BaseSchema):
    """Schema for book with character information."""
    
    book: BookResponse = Field(..., description="Book information")
    characters: List[dict] = Field(..., description="List of characters")
    pov_characters: List[dict] = Field(..., description="List of POV characters")


class BookOverview(BaseSchema):
    """Schema for book overview with statistics."""
    
    total_books: int = Field(..., description="Total number of books")
    standalone_books: int = Field(..., description="Number of standalone books")
    books_with_series: int = Field(..., description="Number of books with series")
    books_by_world: dict = Field(..., description="Books grouped by world")
    books: List[BookResponse] = Field(..., description="List of books")


class ReadingOrder(BaseSchema):
    """Schema for reading order information."""
    
    book: BookResponse = Field(..., description="Book information")
    order: int = Field(..., description="Reading order")
    is_published: bool = Field(..., description="Whether the book is published")
