"""
CharacterRelationship model for character relationships.
"""
from sqlalchemy import Column, String, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class RelationshipType(enum.Enum):
    """Relationship type enumeration."""
    FAMILY = "family"
    ROMANTIC = "romantic"
    FRIENDSHIP = "friendship"
    ENEMY = "enemy"
    MENTOR = "mentor"
    STUDENT = "student"
    ALLY = "ally"
    RIVAL = "rival"
    OTHER = "other"


class CharacterRelationship(BaseModel):
    """CharacterRelationship model representing relationships between characters."""
    
    __tablename__ = "character_relationships"
    
    id = Column(String(50), primary_key=True, index=True)
    character_id = Column(String(50), ForeignKey("characters.id"), nullable=False, index=True)
    related_character_id = Column(String(50), ForeignKey("characters.id"), nullable=False, index=True)
    relationship_type = Column(Enum(RelationshipType), nullable=False)
    description = Column(Text, nullable=True)
    is_reciprocal = Column(Boolean, default=False)  # Is this relationship mutual
    strength = Column(String(50), nullable=True)  # strong, weak, etc.
    notes = Column(Text, nullable=True)
    
    # Relationships
    character = relationship("Character", 
                           foreign_keys=[character_id],
                           back_populates="relationships")
    related_character = relationship("Character",
                                   foreign_keys=[related_character_id],
                                   back_populates="related_characters")
    
    def __repr__(self):
        return f"<CharacterRelationship(character_id='{self.character_id}', related_character_id='{self.related_character_id}', type='{self.relationship_type.value}')>"
    
    @classmethod
    def get_by_character(cls, db, character_id):
        """Get all relationships for a character."""
        return db.query(cls).filter(cls.character_id == character_id).all()
    
    @classmethod
    def get_by_type(cls, db, character_id, relationship_type):
        """Get relationships of a specific type for a character."""
        return db.query(cls).filter(
            cls.character_id == character_id,
            cls.relationship_type == relationship_type
        ).all()
    
    @classmethod
    def get_between_characters(cls, db, character1_id, character2_id):
        """Get relationships between two specific characters."""
        return db.query(cls).filter(
            ((cls.character_id == character1_id) & (cls.related_character_id == character2_id)) |
            ((cls.character_id == character2_id) & (cls.related_character_id == character1_id))
        ).all() 