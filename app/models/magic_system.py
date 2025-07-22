from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class MagicSystem(BaseModel):
    """MagicSystem model representing magic systems in the Cosmere."""
    
    __tablename__ = "magic_systems"
    
    # Basic information
    name = Column(String(255), nullable=False, index=True)
    type = Column(String(100), nullable=False, index=True)  # allomancy, feruchemy, hemalurgy, surgebinding, etc.
    power_source = Column(String(255), nullable=True)
    
    # Relationships
    world_id = Column(String(36), ForeignKey("worlds.id"), nullable=True, index=True)
    
    # Detailed information
    description = Column(Text, nullable=True)
    mechanics = Column(Text, nullable=True)  # Store as JSON string
    limitations = Column(Text, nullable=True)  # Store as JSON string
    
    # Relationships
    world = relationship("World", back_populates="magic_systems")
    
    def __repr__(self):
        return f"<MagicSystem(name='{self.name}', type='{self.type}', world='{self.world.name if self.world else None}')>"
    
    @property
    def has_mechanics(self) -> bool:
        """Check if this magic system has defined mechanics."""
        return bool(self.mechanics and len(self.mechanics) > 0)
    
    @property
    def has_limitations(self) -> bool:
        """Check if this magic system has defined limitations."""
        return bool(self.limitations and len(self.limitations) > 0)
    
    def get_mechanics_list(self) -> list:
        """Get a list of mechanics."""
        if not self.mechanics:
            return []
        return list(self.mechanics.keys())
    
    def get_limitations_list(self) -> list:
        """Get a list of limitations."""
        if not self.limitations:
            return []
        return list(self.limitations.keys())
    
    def to_dict(self) -> dict:
        """Convert magic system to dictionary with additional computed fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "has_mechanics": self.has_mechanics,
            "has_limitations": self.has_limitations,
            "mechanics_list": self.get_mechanics_list(),
            "limitations_list": self.get_limitations_list(),
        })
        return base_dict
    
    @classmethod
    def get_by_world(cls, db, world_id: str):
        """Get all magic systems from a specific world."""
        return db.query(cls).filter(cls.world_id == world_id).all()
    
    @classmethod
    def get_by_type(cls, db, magic_type: str):
        """Get magic systems by type."""
        return db.query(cls).filter(cls.type == magic_type).all()
    
    @classmethod
    def search_by_name(cls, db, name: str):
        """Search magic systems by name (case-insensitive)."""
        return db.query(cls).filter(
            cls.name.ilike(f"%{name}%")
        ).all()
    
    @classmethod
    def get_with_mechanics(cls, db):
        """Get magic systems that have defined mechanics."""
        return db.query(cls).filter(cls.mechanics.isnot(None)).all()
    
    @classmethod
    def get_by_power_source(cls, db, power_source: str):
        """Get magic systems by power source."""
        return db.query(cls).filter(cls.power_source == power_source).all() 