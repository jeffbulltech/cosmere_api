from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import uuid
from .base import BaseSchema, PaginatedResponse


class BookBase(BaseSchema):
    """Base book schema with common fields."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Book title")
    isbn: Optional[str] = Field(default=None, max_length=20, description="ISBN")
    publication_date: Optional[date] = Field(default=None, description="Publication date")
    word_count: Optional[int] = Field(default=None, ge=0, description="Word count")
    chronological_order: Optional[int] = Field(default=None, ge=0, description="Chronological order")
    summary: Optional[str] = Field(default=None, description="Book summary")
    cosmere_significance: Optional[Dict[str, Any]] = Field(default=None, description="Cosmere significance")


class BookCreate(BookBase):
    """Schema for creating a new book."""
    
    world_id: str = Field(..., description="World ID")
    series_id: Optional[str] = Field(default=None, description="Series ID")


class BookUpdate(BaseSchema):
    """Schema for updating a book."""
    
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(default=None, max_length=20)
    publication_date: Optional[date] = Field(default=None)
    word_count: Optional[int] = Field(default=None, ge=0)
    chronological_order: Optional[int] = Field(default=None, ge=0)
    world_id: Optional[str] = Field(default=None)
    series_id: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    cosmere_significance: Optional[Dict[str, Any]] = Field(default=None)


class BookResponse(BookBase):
    """Schema for book response."""
    
    id: str
    world_id: str
    series_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    character_count: int
    publication_year: Optional[int] = None
    is_part_of_series: bool
    
    # Related data (optional)
    world: Optional[Dict[str, Any]] = None
    series: Optional[Dict[str, Any]] = None
    characters: Optional[List[Dict[str, Any]]] = None


class BookList(BaseSchema):
    """Schema for book list response."""
    
    id: str
    title: str
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    chronological_order: Optional[int] = None
    world_id: str
    series_id: Optional[str] = None
    character_count: int
    publication_year: Optional[int] = None
    is_part_of_series: bool
    created_at: datetime


class BookDetail(BookResponse):
    """Schema for detailed book response."""
    
    # Include all relationships
    world: Dict[str, Any]
    series: Optional[Dict[str, Any]] = None
    characters: List[Dict[str, Any]]


class BookFilters(BaseSchema):
    """Schema for book filters."""
    
    series_id: Optional[str] = Field(default=None, description="Filter by series")
    world_id: Optional[str] = Field(default=None, description="Filter by world")
    publication_year: Optional[int] = Field(default=None, description="Filter by publication year")
    chronological_order: Optional[int] = Field(default=None, description="Filter by chronological order")
    search: Optional[str] = Field(default=None, description="Search by title")


class BookStats(BaseSchema):
    """Schema for book statistics."""
    
    total_books: int
    books_by_series: Dict[str, int]
    books_by_world: Dict[str, int]
    books_by_year: Dict[int, int]
    standalone_books: int
    average_word_count: float
    average_characters_per_book: float
    total_word_count: int


class BookSearchResult(BaseSchema):
    """Schema for book search result."""
    
    id: str
    title: str
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    world_name: str
    series_name: Optional[str] = None
    character_count: int
    word_count: Optional[int] = None
    summary: Optional[str] = None
    score: Optional[float] = None  # Search relevance score


class BookCharacterRole(BaseSchema):
    """Schema for character role in a book."""
    
    character_id: str
    book_id: str
    role: str  # protagonist, antagonist, supporting, minor
    character_name: str
    character_world: str


class BookTimeline(BaseSchema):
    """Schema for book timeline."""
    
    chronological_order: int
    title: str
    publication_date: Optional[date] = None
    world_name: str
    series_name: Optional[str] = None
    character_count: int
    word_count: Optional[int] = None


# Paginated response types
BookPaginatedResponse = PaginatedResponse[BookList] 