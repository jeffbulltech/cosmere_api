from sqlalchemy import Column, String, Text, Integer, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import date


# Association table for many-to-many relationship between books and characters
book_characters = Table(
    'book_characters',
    BaseModel.metadata,
    Column('book_id', String(36), ForeignKey('books.id'), primary_key=True),
    Column('character_id', String(36), ForeignKey('characters.id'), primary_key=True),
    Column('role', String(100), nullable=True),  # protagonist, antagonist, supporting, etc.
)


class Book(BaseModel):
    """Book model representing books in the Cosmere."""
    
    __tablename__ = "books"
    
    # Basic information
    title = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), nullable=True, unique=True)
    publication_date = Column(Date, nullable=True, index=True)
    word_count = Column(Integer, nullable=True)
    chronological_order = Column(Integer, nullable=True, index=True)
    
    # Relationships
    series_id = Column(
        String(36),
        ForeignKey("series.id"),
        nullable=True,
        index=True
    )
    world_id = Column(
        String(36),
        ForeignKey("worlds.id"),
        nullable=False,
        index=True
    )
    
    # Content
    summary = Column(Text, nullable=True)
    cosmere_significance = Column(Text, nullable=True)  # Store as JSON string
    
    # Relationships
    series = relationship("Series", back_populates="books")
    world = relationship("World", back_populates="books")
    characters = relationship(
        "Character",
        secondary=book_characters,
        back_populates="books"
    )
    
    def __repr__(self):
        return f"<Book(title='{self.title}', series='{self.series.name if self.series else None}')>"
    
    @property
    def character_count(self) -> int:
        """Get the number of characters in this book."""
        return len(self.characters) if self.characters else 0
    
    @property
    def publication_year(self) -> int:
        """Get the publication year."""
        return self.publication_date.year if self.publication_date else None
    
    @property
    def is_part_of_series(self) -> bool:
        """Check if this book is part of a series."""
        return self.series_id is not None
    
    def to_dict(self) -> dict:
        """Convert book to dictionary with additional computed fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "character_count": self.character_count,
            "publication_year": self.publication_year,
            "is_part_of_series": self.is_part_of_series,
        })
        return base_dict
    
    @classmethod
    def get_by_series(cls, db, series_id: str):
        """Get all books in a specific series."""
        return db.query(cls).filter(
            cls.series_id == series_id
        ).order_by(cls.chronological_order).all()
    
    @classmethod
    def get_by_world(cls, db, world_id: str):
        """Get all books set on a specific world."""
        return db.query(cls).filter(
            cls.world_id == world_id
        ).order_by(cls.publication_date).all()
    
    @classmethod
    def get_by_publication_year(cls, db, year: int):
        """Get books published in a specific year."""
        return db.query(cls).filter(
            cls.publication_date >= date(year, 1, 1),
            cls.publication_date < date(year + 1, 1, 1)
        ).all()
    
    @classmethod
    def get_chronological_order(cls, db):
        """Get all books in chronological order."""
        return db.query(cls).filter(
            cls.chronological_order.isnot(None)
        ).order_by(cls.chronological_order).all()
    
    @classmethod
    def search_by_title(cls, db, title: str):
        """Search books by title (case-insensitive)."""
        return db.query(cls).filter(
            cls.title.ilike(f"%{title}%")
        ).all()
    
    @classmethod
    def get_standalone_books(cls, db):
        """Get books that are not part of a series."""
        return db.query(cls).filter(cls.series_id.is_(None)).all() 