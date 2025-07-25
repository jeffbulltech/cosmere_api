"""
Character model for Cosmere characters.
"""
from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class CharacterStatus(enum.Enum):
    """Character status enumeration."""
    ALIVE = "alive"
    DEAD = "dead"
    UNKNOWN = "unknown"
    IMMORTAL = "immortal"


class Character(BaseModel):
    """Character model representing a Cosmere character."""
    
    __tablename__ = "characters"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    aliases = Column(Text, nullable=True)  # JSON string of aliases
    world_of_origin_id = Column(String(36), ForeignKey("worlds.id"), nullable=False, index=True)
    species = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)
    first_appearance_book_id = Column(String(36), ForeignKey("books.id"), nullable=True, index=True)
    biography = Column(Text, nullable=True)
    magic_abilities = Column(Text, nullable=True)  # JSON string
    affiliations = Column(Text, nullable=True)  # JSON string
    cosmere_significance = Column(Text, nullable=True)  # JSON string
    
    # Relationships
    world_of_origin = relationship("World", back_populates="characters")
    first_appearance_book = relationship("Book", foreign_keys=[first_appearance_book_id])
    books = relationship("BookCharacter", back_populates="character")
    relationships = relationship("CharacterRelationship", 
                               foreign_keys="CharacterRelationship.character_id",
                               back_populates="character")
    related_characters = relationship("CharacterRelationship",
                                    foreign_keys="CharacterRelationship.related_character_id",
                                    back_populates="related_character")
    magic_systems = relationship("CharacterMagicSystem", back_populates="character")
    
    def __repr__(self):
        return f"<Character(id='{self.id}', name='{self.name}')>"
    
    @classmethod
    def get_by_name(cls, db, name):
        """Get character by name."""
        return db.query(cls).filter(cls.name == name).first()
    
    @classmethod
    def get_by_alias(cls, db, alias):
        """Get character by alias."""
        return db.query(cls).filter(cls.aliases.contains([alias])).all()
    
    @classmethod
    def get_by_world(cls, db, world_id):
        """Get characters by world of origin."""
        return db.query(cls).filter(cls.world_of_origin_id == world_id).all()
    
    @classmethod
    def get_by_species(cls, db, species):
        """Get characters by species."""
        return db.query(cls).filter(cls.species == species).all()
    
    @classmethod
    def get_by_status(cls, db, status):
        """Get characters by status."""
        return db.query(cls).filter(cls.status == status).all()
    
    @classmethod
    def search_by_name(cls, db, search_term):
        """Search characters by name or aliases."""
        return db.query(cls).filter(
            (cls.name.ilike(f"%{search_term}%")) |
            (cls.aliases.any(lambda x: search_term.lower() in x.lower()))
        ).all()
