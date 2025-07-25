"""
Shard model for Shards of Adonalsium.
"""
from sqlalchemy import Column, String, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class ShardStatus(enum.Enum):
    """Shard status enumeration."""
    WHOLE = "whole"
    SPLINTERED = "splintered"
    CONJOINED = "conjoined"
    UNKNOWN = "unknown"


class Shard(BaseModel):
    """Shard model representing a Shard of Adonalsium."""
    
    __tablename__ = "shards"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    intent = Column(String(100), nullable=True)  # The Shard's intent
    status = Column(Enum(ShardStatus), default=ShardStatus.UNKNOWN)
    current_vessel = Column(String(100), nullable=True)  # Current vessel name
    original_vessel = Column(String(100), nullable=True)  # Original vessel name
    description = Column(Text, nullable=True)
    perpendicularity = Column(Text, nullable=True)  # Location of perpendicularity
    magic_systems = Column(Text, nullable=True)  # Associated magic systems
    residence = Column(Text, nullable=True)  # Where the Shard resides
    is_combined = Column(Boolean, default=False)  # Is this a combination of Shards
    
    # Relationships
    vessels = relationship("ShardVessel", back_populates="shard")
    worlds = relationship("World", back_populates="shard")
    
    def __repr__(self):
        return f"<Shard(id='{self.id}', name='{self.name}', intent='{self.intent}')>"
    
    @classmethod
    def get_by_name(cls, db, name):
        """Get shard by name."""
        return db.query(cls).filter(cls.name == name).first()
    
    @classmethod
    def get_by_intent(cls, db, intent):
        """Get shards by intent."""
        return db.query(cls).filter(cls.intent == intent).all()
    
    @classmethod
    def get_by_status(cls, db, status):
        """Get shards by status."""
        return db.query(cls).filter(cls.status == status).all()
    
    @classmethod
    def get_by_vessel(cls, db, vessel_name):
        """Get shards by vessel name."""
        return db.query(cls).filter(
            (cls.current_vessel == vessel_name) |
            (cls.original_vessel == vessel_name)
        ).all()
    
    @classmethod
    def get_combined_shards(cls, db):
        """Get combined shards."""
        return db.query(cls).filter(cls.is_combined == True).all()


class ShardVessel(BaseModel):
    """Shard Vessel model representing vessels of Shards."""
    
    __tablename__ = "shard_vessels"
    
    id = Column(String(50), primary_key=True, index=True)
    shard_id = Column(String(50), ForeignKey("shards.id"), nullable=False, index=True)
    vessel_name = Column(String(100), nullable=False)
    vessel_type = Column(String(50), nullable=True)  # original, current, former
    start_date = Column(String(50), nullable=True)  # When they became vessel
    end_date = Column(String(50), nullable=True)  # When they stopped being vessel
    description = Column(Text, nullable=True)
    
    # Relationships
    shard = relationship("Shard", back_populates="vessels")
    
    def __repr__(self):
        return f"<ShardVessel(shard_id='{self.shard_id}', vessel_name='{self.vessel_name}')>" 