"""
World model for Cosmere worlds.
"""
from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class World(BaseModel):
    """World model representing a Cosmere world."""
    
    __tablename__ = "worlds"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    system = Column(String(255), nullable=True)  # Planetary system
    shard_id = Column(String(36), ForeignKey("shards.id"), nullable=True, index=True)
    geography = Column(Text, nullable=True)  # JSON string
    culture_notes = Column(Text, nullable=True)
    technology_level = Column(String(100), nullable=True)
    
    # Relationships
    shard = relationship("Shard", foreign_keys=[shard_id], back_populates="worlds")
    books = relationship("Book", back_populates="world")
    characters = relationship("Character", back_populates="world_of_origin")
    magic_systems = relationship("MagicSystem", back_populates="world")
    
    def __repr__(self):
        return f"<World(id='{self.id}', name='{self.name}')>"
    
    @classmethod
    def get_by_name(cls, db, name):
        """Get world by name."""
        return db.query(cls).filter(cls.name == name).first()
    
    @classmethod
    def get_by_system(cls, db, system):
        """Get worlds by planetary system."""
        return db.query(cls).filter(cls.system == system).all()
