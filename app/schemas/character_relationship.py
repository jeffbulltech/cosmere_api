from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from .base import BaseSchema


class CharacterRelationshipBase(BaseSchema):
    """Base character relationship schema with common fields."""
    
    character_id: str = Field(..., description="Character ID")
    related_character_id: str = Field(..., description="Related character ID")
    relationship_type: str = Field(..., min_length=1, max_length=100, description="Relationship type")
    description: Optional[str] = Field(default=None, description="Description")
    book_context_id: Optional[str] = Field(default=None, description="Book context ID")


class CharacterRelationshipCreate(CharacterRelationshipBase):
    """Schema for creating a new character relationship."""
    pass


class CharacterRelationshipUpdate(BaseSchema):
    """Schema for updating a character relationship."""
    
    relationship_type: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None)
    book_context_id: Optional[str] = Field(default=None)


class CharacterRelationshipResponse(CharacterRelationshipBase):
    """Schema for character relationship response."""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    # Computed fields
    is_positive_relationship: bool
    is_negative_relationship: bool
    is_neutral_relationship: bool
    
    # Related data (optional)
    character: Optional[Dict[str, Any]] = None
    related_character: Optional[Dict[str, Any]] = None
    book_context: Optional[Dict[str, Any]] = None 