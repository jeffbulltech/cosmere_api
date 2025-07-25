"""
Series repository for data access operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.series import Series, SeriesStatus
from app.repositories.base import BaseRepository


class SeriesRepository(BaseRepository[Series]):
    """Repository for Series model operations."""
    
    def __init__(self, db: Session):
        super().__init__(Series, db)
    
    def get_by_name(self, name: str) -> Optional[Series]:
        """Get series by name."""
        return self.get_by_field("name", name)
    
    def get_by_world(self, world_id: str) -> List[Series]:
        """Get series by world."""
        return self.get_by_field_multi("world_id", world_id)
    
    def get_by_status(self, status: SeriesStatus) -> List[Series]:
        """Get series by status."""
        return self.get_multi(filters={"status": status})
    
    def get_ongoing_series(self) -> List[Series]:
        """Get ongoing series."""
        return self.get_by_status(SeriesStatus.ONGOING)
    
    def get_completed_series(self) -> List[Series]:
        """Get completed series."""
        return self.get_by_status(SeriesStatus.COMPLETE)
    
    def search_series(self, search_term: str) -> List[Series]:
        """Search series by name and description."""
        return self.search(search_term, ["name", "description"])
    
    def get_series_with_books(self, series_id: str) -> Optional[dict]:
        """Get a series with its books."""
        series = self.get(series_id)
        if not series:
            return None
        
        return {
            "series": series,
            "books": series.books,
            "world": series.world,
            "total_books": len(series.books),
            "completed_books": len([b for b in series.books if b.publication_date])
        }
    
    def get_series_summary(self) -> List[dict]:
        """Get summary of all series with book counts."""
        series_list = self.get_multi()
        summaries = []
        
        for series in series_list:
            summaries.append({
                "series": series,
                "book_count": len(series.books),
                "world": series.world,
                "completion_percentage": (len(series.books) / series.planned_books * 100) if series.planned_books else 0
            })
        
        return summaries 