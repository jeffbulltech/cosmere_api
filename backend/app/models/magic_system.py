"""
Magic System model for Cosmere magic systems.
"""
from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class MagicSystem(BaseModel):
    """Magic System model representing a Cosmere magic system."""
    
    __tablename__ = "magic_systems"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    world_id = Column(String(50), ForeignKey("worlds.id"), nullable=True, index=True)
    description = Column(Text, nullable=True)
    mechanics = Column(Text, nullable=True)  # How the magic works
    requirements = Column(Text, nullable=True)  # Requirements to use the magic
    limitations = Column(Text, nullable=True)  # Limitations of the magic
    is_investiture_based = Column(Boolean, default=True)
    related_systems = Column(Text, nullable=True)  # JSON string of related magic systems
    
    # Relationships
    world = relationship("World", back_populates="magic_systems")
    users = relationship("CharacterMagicSystem", back_populates="magic_system")
    
    def __repr__(self):
        return f"<MagicSystem(id='{self.id}', name='{self.name}')>"
    
    @classmethod
    def get_by_name(cls, db, name):
        """Get magic system by name."""
        return db.query(cls).filter(cls.name == name).first()
    
    @classmethod
    def get_by_world(cls, db, world_id):
        """Get magic systems by world."""
        return db.query(cls).filter(cls.world_id == world_id).all()
    
    @classmethod
    def get_investiture_based(cls, db):
        """Get investiture-based magic systems."""
        return db.query(cls).filter(cls.is_investiture_based == True).all()
    
    @classmethod
    def search_by_name(cls, db, search_term):
        """Search magic systems by name."""
        return db.query(cls).filter(cls.name.ilike(f"%{search_term}%")).all()
