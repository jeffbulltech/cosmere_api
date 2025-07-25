"""
Book service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.repositories.book_repository import BookRepository
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class BookService(BaseService[BookRepository]):
    """Service for Book business logic."""
    
    def __init__(self, repository: BookRepository):
        super().__init__(repository)
    
    def get_book_by_title(self, title: str) -> Optional[Any]:
        """Get book by title."""
        return self.repository.get_by_title(title)
    
    def get_books_by_series(self, series_id: str) -> List[Any]:
        """Get books by series."""
        return self.repository.get_by_series(series_id)
    
    def get_books_by_world(self, world_id: str) -> List[Any]:
        """Get books by world."""
        return self.repository.get_by_world(world_id)
    
    def get_standalone_books(self) -> List[Any]:
        """Get standalone books."""
        return self.repository.get_standalone_books()
    
    def search_books(self, search_term: str) -> List[Any]:
        """Search books by title and summary."""
        return self.repository.search_books(search_term)
    
    def get_book_with_characters(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Get a book with its characters."""
        return self.repository.get_books_with_characters(book_id)
    
    def get_books_by_publication_date(self, start_date=None, end_date=None) -> List[Any]:
        """Get books by publication date range."""
        return self.repository.get_books_by_publication_date(start_date, end_date)
    
    def get_books_with_series_info(self) -> List[Dict[str, Any]]:
        """Get books with series information."""
        return self.repository.get_books_with_series_info()
    
    def get_books_overview(self) -> Dict[str, Any]:
        """Get an overview of all books with statistics."""
        books = self.get_multi()
        
        total_books = len(books)
        standalone_books = len([b for b in books if b.is_standalone])
        books_with_series = len([b for b in books if b.series_id])
        
        # Group by world
        books_by_world = {}
        for book in books:
            world_name = book.world.name if book.world else "Unknown"
            if world_name not in books_by_world:
                books_by_world[world_name] = 0
            books_by_world[world_name] += 1
        
        return {
            "total_books": total_books,
            "standalone_books": standalone_books,
            "books_with_series": books_with_series,
            "books_by_world": books_by_world,
            "books": books
        }
    
    def get_reading_order(self, series_id: str) -> List[Dict[str, Any]]:
        """Get reading order for a series."""
        books = self.get_books_by_series(series_id)
        
        # Sort by reading order if available, otherwise by publication date
        sorted_books = sorted(
            books, 
            key=lambda x: (x.reading_order or 0, x.publication_date or "9999-12-31")
        )
        
        return [
            {
                "book": book,
                "order": i + 1,
                "is_published": book.publication_date is not None
            }
            for i, book in enumerate(sorted_books)
        ] 