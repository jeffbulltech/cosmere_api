"""
Book repository for data access operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.book import Book
from app.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    """Repository for Book model operations."""
    
    def __init__(self, db: Session):
        super().__init__(Book, db)
    
    def get_by_title(self, title: str) -> Optional[Book]:
        """Get book by title."""
        return self.get_by_field("title", title)
    
    def get_by_series(self, series_id: str) -> List[Book]:
        """Get books by series."""
        return self.get_by_field_multi("series_id", series_id)
    
    def get_by_world(self, world_id: str) -> List[Book]:
        """Get books by world."""
        return self.get_by_field_multi("world_id", world_id)
    
    def get_standalone_books(self) -> List[Book]:
        """Get standalone books."""
        return self.get_multi(filters={"is_standalone": True})
    
    def search_books(self, search_term: str) -> List[Book]:
        """Search books by title and summary."""
        return self.search(search_term, ["title", "summary"])
    
    def get_books_with_characters(self, book_id: str) -> Optional[dict]:
        """Get a book with its characters."""
        book = self.get(book_id)
        if not book:
            return None
        
        return {
            "book": book,
            "characters": [bc.character for bc in book.characters],
            "pov_characters": [bc.character for bc in book.characters if bc.is_pov_character]
        }
    
    def get_books_by_publication_date(self, start_date=None, end_date=None) -> List[Book]:
        """Get books by publication date range."""
        query = self.db.query(Book)
        
        if start_date:
            query = query.filter(Book.publication_date >= start_date)
        if end_date:
            query = query.filter(Book.publication_date <= end_date)
        
        return query.order_by(Book.publication_date).all()
    
    def get_books_with_series_info(self) -> List[dict]:
        """Get books with series information."""
        books = self.db.query(Book).join(Book.series).all()
        return [
            {
                "book": book,
                "series": book.series,
                "world": book.world
            }
            for book in books
        ] 