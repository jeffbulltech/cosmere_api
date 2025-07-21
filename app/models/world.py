from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from typing import List, Optional


class World(BaseModel):
    """World model representing planets and locations in the Cosmere."""
    
    __tablename__ = "worlds"
    
    # Basic information
    name = Column(String(255), nullable=False, unique=True, index=True)
    system = Column(String(255), nullable=True, index=True)
    
    # Shard relationship (optional - some worlds may not have shards)
    shard_id = Column(
        String(36),
        ForeignKey("shards.id"),
        nullable=True,
        index=True
    )
    
    # Geographic and cultural information
    geography = Column(Text, nullable=True)
    culture_notes = Column(Text, nullable=True)
    technology_level = Column(String(100), nullable=True, index=True)
    
    # Relationships
    shard = relationship("Shard", foreign_keys=[shard_id])
    books = relationship("Book", back_populates="world")
    characters = relationship("Character", back_populates="world_of_origin")
    magic_systems = relationship("MagicSystem", back_populates="world")
    
    def __repr__(self):
        return f"<World(name='{self.name}', system='{self.system}')>"
    
    @property
    def has_shard(self) -> bool:
        """Check if this world has a shard."""
        return self.shard_id is not None
    
    @property
    def character_count(self) -> int:
        """Get the number of characters from this world."""
        return len(self.characters) if self.characters else 0
    
    @property
    def book_count(self) -> int:
        """Get the number of books set on this world."""
        return len(self.books) if self.books else 0
    
    @property
    def magic_system_count(self) -> int:
        """Get the number of magic systems on this world."""
        return len(self.magic_systems) if self.magic_systems else 0
    
    def to_dict(self) -> dict:
        """Convert world to dictionary with additional computed fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "has_shard": self.has_shard,
            "character_count": self.character_count,
            "book_count": self.book_count,
            "magic_system_count": self.magic_system_count,
        })
        return base_dict
    
    @classmethod
    def get_by_system(cls, db, system: str):
        """Get all worlds in a specific system."""
        return db.query(cls).filter(cls.system == system).all()
    
    @classmethod
    def get_by_technology_level(cls, db, technology_level: str):
        """Get worlds by technology level."""
        return db.query(cls).filter(cls.technology_level == technology_level).all()
    
    @classmethod
    def get_with_shards(cls, db):
        """Get all worlds that have shards."""
        return db.query(cls).filter(cls.shard_id.isnot(None)).all()
    
    @classmethod
    def search_by_name(cls, db, name: str):
        """Search worlds by name (case-insensitive)."""
        return db.query(cls).filter(
            cls.name.ilike(f"%{name}%")
        ).all() 