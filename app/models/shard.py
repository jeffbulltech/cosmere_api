from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Shard(BaseModel):
    """Shard model representing the Shards of Adonalsium."""
    
    __tablename__ = "shards"
    
    # Basic information
    name = Column(String(255), nullable=False, unique=True, index=True)
    intent = Column(String(255), nullable=False, index=True)
    vessel_name = Column(String(255), nullable=True)
    vessel_status = Column(String(100), nullable=True, index=True)  # alive, dead, splintered, etc.
    
    # Relationships
    world_location_id = Column(
        String(36),
        ForeignKey("worlds.id"),
        nullable=True,
        index=True
    )
    
    # Detailed information
    description = Column(Text, nullable=True)
    splinter_info = Column(Text, nullable=True)  # Store as JSON string
    
    # Relationships
    world_location = relationship("World", foreign_keys=[world_location_id])
    
    def __repr__(self):
        return f"<Shard(name='{self.name}', intent='{self.intent}')>"
    
    @property
    def is_splintered(self) -> bool:
        """Check if this shard is splintered."""
        return self.vessel_status == "splintered"
    
    @property
    def is_alive(self) -> bool:
        """Check if this shard's vessel is alive."""
        return self.vessel_status == "alive"
    
    @property
    def has_world_location(self) -> bool:
        """Check if this shard has a world location."""
        return self.world_location_id is not None
    
    @property
    def world_count(self) -> int:
        """Get the number of worlds associated with this shard."""
        return len(self.worlds) if self.worlds else 0
    
    def get_splinter_info_list(self) -> list:
        """Get a list of splinter information."""
        if not self.splinter_info:
            return []
        return list(self.splinter_info.keys())
    
    def to_dict(self) -> dict:
        """Convert shard to dictionary with additional computed fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "is_splintered": self.is_splintered,
            "is_alive": self.is_alive,
            "has_world_location": self.has_world_location,
            "world_count": self.world_count,
            "splinter_info_list": self.get_splinter_info_list(),
        })
        return base_dict
    
    @classmethod
    def get_by_intent(cls, db, intent: str):
        """Get shards by intent."""
        return db.query(cls).filter(cls.intent == intent).all()
    
    @classmethod
    def get_by_vessel_status(cls, db, status: str):
        """Get shards by vessel status."""
        return db.query(cls).filter(cls.vessel_status == status).all()
    
    @classmethod
    def get_alive_shards(cls, db):
        """Get shards with alive vessels."""
        return db.query(cls).filter(cls.vessel_status == "alive").all()
    
    @classmethod
    def get_splintered_shards(cls, db):
        """Get splintered shards."""
        return db.query(cls).filter(cls.vessel_status == "splintered").all()
    
    @classmethod
    def search_by_name(cls, db, name: str):
        """Search shards by name (case-insensitive)."""
        return db.query(cls).filter(
            cls.name.ilike(f"%{name}%")
        ).all()
    
    @classmethod
    def get_with_world_locations(cls, db):
        """Get shards that have world locations."""
        return db.query(cls).filter(cls.world_location_id.isnot(None)).all() 