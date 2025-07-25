"""
Book model for Cosmere books.
"""
from datetime import date
from sqlalchemy import Column, String, Text, Date, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Book(BaseModel):
    """Book model representing a Cosmere book."""
    
    __tablename__ = "books"
    
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), nullable=True, unique=True)
    publication_date = Column(Date, nullable=True)
    word_count = Column(Integer, nullable=True)
    chronological_order = Column(Integer, nullable=True, index=True)
    series_id = Column(String(36), ForeignKey("series.id"), nullable=True, index=True)
    world_id = Column(String(36), ForeignKey("worlds.id"), nullable=False, index=True)
    summary = Column(Text, nullable=True)
    cosmere_significance = Column(Text, nullable=True)
    
    # Relationships
    series = relationship("Series", back_populates="books")
    world = relationship("World", back_populates="books")
    characters = relationship("BookCharacter", back_populates="book")
    first_appearance_characters = relationship("Character", foreign_keys="Character.first_appearance_book_id")
    
    def __repr__(self):
        return f"<Book(id='{self.id}', title='{self.title}')>"
    
    @classmethod
    def get_by_title(cls, db, title):
        """Get book by title."""
        return db.query(cls).filter(cls.title == title).first()
    
    @classmethod
    def get_by_series(cls, db, series_id):
        """Get books by series."""
        return db.query(cls).filter(cls.series_id == series_id).order_by(cls.reading_order).all()
    
    @classmethod
    def get_by_world(cls, db, world_id):
        """Get books by world."""
        return db.query(cls).filter(cls.world_id == world_id).all()
    
    @classmethod
    def get_standalone(cls, db):
        """Get standalone books."""
        return db.query(cls).filter(cls.is_standalone == True).all()
    
    @classmethod
    def search_by_title(cls, db, search_term):
        """Search books by title."""
        return db.query(cls).filter(cls.title.ilike(f"%{search_term}%")).all()
