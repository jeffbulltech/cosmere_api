"""
Series model for book series.
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class SeriesStatus(enum.Enum):
    """Series status enumeration."""
    ONGOING = "ongoing"
    COMPLETE = "complete"
    PLANNED = "planned"
    ON_HIATUS = "on_hiatus"


class Series(BaseModel):
    """Series model representing a book series."""
    
    __tablename__ = "series"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    world_id = Column(String(50), ForeignKey("worlds.id"), nullable=True, index=True)
    planned_books = Column(Integer, nullable=True)
    current_books = Column(Integer, default=0)
    status = Column(Enum(SeriesStatus), default=SeriesStatus.ONGOING)
    reading_order = Column(Text, nullable=True)  # JSON string for reading order
    
    # Relationships
    world = relationship("World", foreign_keys=[world_id])
    books = relationship("Book", back_populates="series", order_by="Book.publication_date")
    
    def __repr__(self):
        return f"<Series(id='{self.id}', name='{self.name}', status='{self.status.value}')>"
    
    @classmethod
    def get_by_name(cls, db, name):
        """Get series by name."""
        return db.query(cls).filter(cls.name == name).first()
    
    @classmethod
    def get_by_status(cls, db, status):
        """Get series by status."""
        return db.query(cls).filter(cls.status == status).all()
    
    @classmethod
    def get_by_world(cls, db, world_id):
        """Get series by world."""
        return db.query(cls).filter(cls.world_id == world_id).all() 