from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Series(BaseModel):
    """Series model representing book series in the Cosmere."""
    
    __tablename__ = "series"
    
    # Basic information
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    books = relationship("Book", back_populates="series", order_by="Book.chronological_order")
    
    def __repr__(self):
        return f"<Series(name='{self.name}')>"
    
    @property
    def book_count(self) -> int:
        """Get the number of books in this series."""
        return len(self.books) if self.books else 0
    
    @property
    def total_word_count(self) -> int:
        """Get the total word count of all books in the series."""
        return sum(book.word_count or 0 for book in self.books) if self.books else 0
    
    @property
    def worlds(self) -> list:
        """Get unique worlds featured in this series."""
        if not self.books:
            return []
        return list(set(book.world for book in self.books if book.world))
    
    def to_dict(self) -> dict:
        """Convert series to dictionary with additional computed fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "book_count": self.book_count,
            "total_word_count": self.total_word_count,
            "worlds": [world.to_dict() for world in self.worlds],
        })
        return base_dict
    
    @classmethod
    def search_by_name(cls, db, name: str):
        """Search series by name (case-insensitive)."""
        return db.query(cls).filter(
            cls.name.ilike(f"%{name}%")
        ).all()
    
    @classmethod
    def get_with_books(cls, db):
        """Get all series that have books."""
        return db.query(cls).filter(cls.books.any()).all() 