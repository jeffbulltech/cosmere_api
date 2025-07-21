from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from .base import BaseSchema, PaginatedResponse


class CharacterBase(BaseSchema):
    """Base character schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Character name")
    aliases: Optional[List[str]] = Field(default=None, description="Character aliases")
    species: Optional[str] = Field(default=None, max_length=100, description="Character species")
    status: Optional[str] = Field(default="unknown", max_length=50, description="Character status")
    biography: Optional[str] = Field(default=None, description="Character biography")
    magic_abilities: Optional[Dict[str, Any]] = Field(default=None, description="Magic abilities")
    affiliations: Optional[Dict[str, Any]] = Field(default=None, description="Affiliations")
    cosmere_significance: Optional[Dict[str, Any]] = Field(default=None, description="Cosmere significance")


class CharacterCreate(CharacterBase):
    """Schema for creating a new character."""
    
    world_of_origin_id: str = Field(..., description="World of origin ID")
    first_appearance_book_id: Optional[str] = Field(default=None, description="First appearance book ID")


class CharacterUpdate(BaseSchema):
    """Schema for updating a character."""
    
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    aliases: Optional[List[str]] = Field(default=None)
    species: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(default=None, max_length=50)
    world_of_origin_id: Optional[str] = Field(default=None)
    first_appearance_book_id: Optional[str] = Field(default=None)
    biography: Optional[str] = Field(default=None)
    magic_abilities: Optional[Dict[str, Any]] = Field(default=None)
    affiliations: Optional[Dict[str, Any]] = Field(default=None)
    cosmere_significance: Optional[Dict[str, Any]] = Field(default=None)


class CharacterResponse(CharacterBase):
    """Schema for character response."""
    
    id: str
    world_of_origin_id: str
    first_appearance_book_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    book_count: int
    relationship_count: int
    has_magic_abilities: bool
    is_alive: bool
    magic_abilities_list: List[str]
    affiliations_list: List[str]
    
    # Related data (optional)
    world_of_origin: Optional[Dict[str, Any]] = None
    first_appearance_book: Optional[Dict[str, Any]] = None
    books: Optional[List[Dict[str, Any]]] = None
    relationships: Optional[List[Dict[str, Any]]] = None


class CharacterList(BaseSchema):
    """Schema for character list response."""
    
    id: str
    name: str
    aliases: Optional[List[str]] = None
    species: Optional[str] = None
    status: Optional[str] = None
    world_of_origin_id: str
    book_count: int
    relationship_count: int
    has_magic_abilities: bool
    is_alive: bool
    created_at: datetime


class CharacterDetail(CharacterResponse):
    """Schema for detailed character response."""
    
    # Include all relationships
    world_of_origin: Dict[str, Any]
    first_appearance_book: Optional[Dict[str, Any]] = None
    books: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]


class CharacterFilters(BaseSchema):
    """Schema for character filters."""
    
    world_id: Optional[str] = Field(default=None, description="Filter by world")
    status: Optional[str] = Field(default=None, description="Filter by status")
    species: Optional[str] = Field(default=None, description="Filter by species")
    magic_ability: Optional[str] = Field(default=None, description="Filter by magic ability")
    affiliation: Optional[str] = Field(default=None, description="Filter by affiliation")
    search: Optional[str] = Field(default=None, description="Search by name or aliases")


class CharacterRelationshipSummary(BaseSchema):
    """Schema for character relationship summary."""
    
    character_id: str
    related_character_id: str
    relationship_type: str
    description: Optional[str] = None
    is_positive: bool
    is_negative: bool
    is_neutral: bool
    book_context: Optional[Dict[str, Any]] = None


class CharacterStats(BaseSchema):
    """Schema for character statistics."""
    
    total_characters: int
    characters_by_status: Dict[str, int]
    characters_by_species: Dict[str, int]
    characters_by_world: Dict[str, int]
    characters_with_magic: int
    average_relationships_per_character: float
    average_books_per_character: float


class CharacterSearchResult(BaseSchema):
    """Schema for character search result."""
    
    id: str
    name: str
    aliases: Optional[List[str]] = None
    species: Optional[str] = None
    status: Optional[str] = None
    world_name: str
    magic_abilities: List[str]
    affiliations: List[str]
    book_count: int
    relationship_count: int
    score: Optional[float] = None  # Search relevance score


# Paginated response types
CharacterPaginatedResponse = PaginatedResponse[CharacterList] 