"""
BookCharacter junction table for many-to-many relationship between books and characters.
"""
from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class BookCharacter(BaseModel):
    """BookCharacter junction table representing character appearances in books."""
    
    __tablename__ = "book_characters"
    
    id = Column(String(50), primary_key=True, index=True)
    book_id = Column(String(50), ForeignKey("books.id"), nullable=False, index=True)
    character_id = Column(String(50), ForeignKey("characters.id"), nullable=False, index=True)
    role = Column(String(100), nullable=True)  # main, supporting, cameo, etc.
    is_pov_character = Column(Boolean, default=False)  # Is this a POV character
    first_appearance = Column(Boolean, default=False)  # Is this their first appearance
    notes = Column(Text, nullable=True)  # Additional notes about the character in this book
    
    # Relationships
    book = relationship("Book", back_populates="characters")
    character = relationship("Character", back_populates="books")
    
    def __repr__(self):
        return f"<BookCharacter(book_id='{self.book_id}', character_id='{self.character_id}')>"
    
    @classmethod
    def get_by_book(cls, db, book_id):
        """Get all characters in a book."""
        return db.query(cls).filter(cls.book_id == book_id).all()
    
    @classmethod
    def get_by_character(cls, db, character_id):
        """Get all books a character appears in."""
        return db.query(cls).filter(cls.character_id == character_id).all()
    
    @classmethod
    def get_pov_characters(cls, db, book_id):
        """Get POV characters in a book."""
        return db.query(cls).filter(
            cls.book_id == book_id,
            cls.is_pov_character == True
        ).all() 