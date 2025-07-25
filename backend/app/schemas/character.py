"""
Character schemas for API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class CharacterBase(BaseSchema):
    """Base character schema with common fields."""
    
    name: str = Field(..., description="Character name", min_length=1, max_length=255)
    aliases: Optional[str] = Field(None, description="Character aliases as JSON string")
    world_of_origin_id: str = Field(..., description="World of origin ID", max_length=36)
    species: Optional[str] = Field(None, description="Character species", max_length=100)
    status: Optional[str] = Field(None, description="Character status", max_length=50)
    first_appearance_book_id: Optional[str] = Field(None, description="First appearance book ID", max_length=36)
    biography: Optional[str] = Field(None, description="Character biography")
    magic_abilities: Optional[str] = Field(None, description="Magic abilities as JSON string")
    affiliations: Optional[str] = Field(None, description="Affiliations as JSON string")
    cosmere_significance: Optional[str] = Field(None, description="Cosmere significance as JSON string")


class CharacterCreate(CharacterBase):
    """Schema for creating a new character."""
    
    id: str = Field(..., description="Character ID", min_length=1, max_length=50)


class CharacterUpdate(BaseModel):
    """Schema for updating a character."""
    
    name: Optional[str] = Field(None, description="Character name", min_length=1, max_length=255)
    aliases: Optional[str] = Field(None, description="Character aliases as JSON string")
    world_of_origin_id: Optional[str] = Field(None, description="World of origin ID", max_length=36)
    species: Optional[str] = Field(None, description="Character species", max_length=100)
    status: Optional[str] = Field(None, description="Character status", max_length=50)
    first_appearance_book_id: Optional[str] = Field(None, description="First appearance book ID", max_length=36)
    biography: Optional[str] = Field(None, description="Character biography")
    magic_abilities: Optional[str] = Field(None, description="Magic abilities as JSON string")
    affiliations: Optional[str] = Field(None, description="Affiliations as JSON string")
    cosmere_significance: Optional[str] = Field(None, description="Cosmere significance as JSON string")


class CharacterResponse(CharacterBase):
    """Schema for character response."""
    
    id: str = Field(..., description="Character ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class CharacterSummary(BaseSchema):
    """Schema for character summary with relationships."""
    
    character: CharacterResponse = Field(..., description="Character information")
    relationships: List[dict] = Field(..., description="Character relationships")
    related_characters: List[dict] = Field(..., description="Related characters")
    books: List[dict] = Field(..., description="Books the character appears in")
    magic_systems: List[dict] = Field(..., description="Magic systems the character uses")


class CharacterNetwork(BaseSchema):
    """Schema for character relationship network."""
    
    character: CharacterResponse = Field(..., description="Character information")
    network: dict = Field(..., description="Network data with nodes and edges")


class CharacterOverview(BaseSchema):
    """Schema for character overview with statistics."""
    
    total_characters: int = Field(..., description="Total number of characters")
    characters_by_world: dict = Field(..., description="Characters grouped by world")
    characters_by_species: dict = Field(..., description="Characters grouped by species")
    characters_by_status: dict = Field(..., description="Characters grouped by status")
    characters: List[CharacterResponse] = Field(..., description="List of characters")
