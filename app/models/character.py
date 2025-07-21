from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.book import book_characters


class Character(BaseModel):
    """Character model representing characters in the Cosmere."""
    
    __tablename__ = "characters"
    
    # Basic information
    name = Column(String(255), nullable=False, index=True)
    aliases = Column(Text, nullable=True)  # Store as JSON string
    species = Column(String(100), nullable=True, index=True)
    status = Column(String(50), nullable=True, index=True)  # alive, dead, cognitive_shadow, etc.
    
    # Relationships
    world_of_origin_id = Column(
        String(36),
        ForeignKey("worlds.id"),
        nullable=False,
        index=True
    )
    first_appearance_book_id = Column(
        String(36),
        ForeignKey("books.id"),
        nullable=True,
        index=True
    )
    
    # Detailed information
    biography = Column(Text, nullable=True)
    magic_abilities = Column(Text, nullable=True)  # Store as JSON string
    affiliations = Column(Text, nullable=True)  # Store as JSON string
    cosmere_significance = Column(Text, nullable=True)  # Store as JSON string
    
    # Relationships
    world_of_origin = relationship("World", back_populates="characters")
    first_appearance_book = relationship("Book")
    books = relationship(
        "Book",
        secondary=book_characters,
        back_populates="characters"
    )
    relationships = relationship(
        "CharacterRelationship",
        foreign_keys="CharacterRelationship.character_id",
        back_populates="character"
    )
    related_characters = relationship(
        "CharacterRelationship",
        foreign_keys="CharacterRelationship.related_character_id",
        back_populates="related_character"
    )
    
    def __repr__(self):
        return f"<Character(name='{self.name}', world='{self.world_of_origin.name if self.world_of_origin else None}')>"
    
    @property
    def book_count(self) -> int:
        """Get the number of books this character appears in."""
        return len(self.books) if self.books else 0
    
    @property
    def relationship_count(self) -> int:
        """Get the number of relationships this character has."""
        return len(self.relationships) if self.relationships else 0
    
    @property
    def has_magic_abilities(self) -> bool:
        """Check if this character has magic abilities."""
        return bool(self.magic_abilities and len(self.magic_abilities) > 0)
    
    @property
    def is_alive(self) -> bool:
        """Check if this character is alive."""
        return self.status == "alive"
    
    def get_magic_abilities_list(self) -> list:
        """Get a list of magic abilities."""
        if not self.magic_abilities:
            return []
        return list(self.magic_abilities.keys())
    
    def get_affiliations_list(self) -> list:
        """Get a list of affiliations."""
        if not self.affiliations:
            return []
        return list(self.affiliations.keys())
    
    def to_dict(self) -> dict:
        """Convert character to dictionary with additional computed fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "book_count": self.book_count,
            "relationship_count": self.relationship_count,
            "has_magic_abilities": self.has_magic_abilities,
            "is_alive": self.is_alive,
            "magic_abilities_list": self.get_magic_abilities_list(),
            "affiliations_list": self.get_affiliations_list(),
        })
        return base_dict
    
    @classmethod
    def get_by_world(cls, db, world_id: str):
        """Get all characters from a specific world."""
        return db.query(cls).filter(cls.world_of_origin_id == world_id).all()
    
    @classmethod
    def get_by_status(cls, db, status: str):
        """Get characters by status."""
        return db.query(cls).filter(cls.status == status).all()
    
    @classmethod
    def get_by_species(cls, db, species: str):
        """Get characters by species."""
        return db.query(cls).filter(cls.species == species).all()
    
    @classmethod
    def get_with_magic_abilities(cls, db):
        """Get characters that have magic abilities."""
        return db.query(cls).filter(cls.magic_abilities.isnot(None)).all()
    
    @classmethod
    def search_by_name(cls, db, name: str):
        """Search characters by name (case-insensitive)."""
        return db.query(cls).filter(
            cls.name.ilike(f"%{name}%")
        ).all()
    
    @classmethod
    def get_by_magic_ability(cls, db, ability: str):
        """Get characters with a specific magic ability."""
        import json
        return db.query(cls).filter(
            cls.magic_abilities.like(f'%"{ability}"%')
        ).all()
    
    @classmethod
    def get_by_affiliation(cls, db, affiliation: str):
        """Get characters with a specific affiliation."""
        import json
        return db.query(cls).filter(
            cls.affiliations.like(f'%"{affiliation}"%')
        ).all() 