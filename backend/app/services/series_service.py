"""
Series service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.repositories.series_repository import SeriesRepository
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class SeriesService(BaseService[SeriesRepository]):
    """Service for Series business logic."""
    
    def __init__(self, repository: SeriesRepository):
        super().__init__(repository)
    
    def get_series_by_name(self, name: str) -> Optional[Any]:
        """Get series by name."""
        return self.repository.get_by_name(name)
    
    def get_series_by_world(self, world_id: str) -> List[Any]:
        """Get series by world."""
        return self.repository.get_by_world(world_id)
    
    def get_series_by_status(self, status: str) -> List[Any]:
        """Get series by status."""
        return self.repository.get_by_status(status)
    
    def get_ongoing_series(self) -> List[Any]:
        """Get ongoing series."""
        return self.repository.get_ongoing_series()
    
    def get_completed_series(self) -> List[Any]:
        """Get completed series."""
        return self.repository.get_completed_series()
    
    def search_series(self, search_term: str) -> List[Any]:
        """Search series by name and description."""
        return self.repository.search_series(search_term)
    
    def get_series_with_books(self, series_id: str) -> Optional[Dict[str, Any]]:
        """Get a series with its books."""
        return self.repository.get_series_with_books(series_id)
    
    def get_series_summary(self) -> List[Dict[str, Any]]:
        """Get summary of all series with book counts."""
        return self.repository.get_series_summary()
    
    def get_series_overview(self) -> Dict[str, Any]:
        """Get an overview of all series with statistics."""
        series_list = self.get_multi()
        
        total_series = len(series_list)
        ongoing_series = len([s for s in series_list if s.status.value == "ongoing"])
        completed_series = len([s for s in series_list if s.status.value == "complete"])
        
        # Group by world
        series_by_world = {}
        for series in series_list:
            world_name = series.world.name if series.world else "Unknown"
            if world_name not in series_by_world:
                series_by_world[world_name] = 0
            series_by_world[world_name] += 1
        
        # Calculate average completion percentage
        completion_percentages = []
        for series in series_list:
            if series.planned_books and series.planned_books > 0:
                completion = (len(series.books) / series.planned_books) * 100
                completion_percentages.append(completion)
        
        avg_completion = sum(completion_percentages) / len(completion_percentages) if completion_percentages else 0
        
        return {
            "total_series": total_series,
            "ongoing_series": ongoing_series,
            "completed_series": completed_series,
            "series_by_world": series_by_world,
            "average_completion_percentage": avg_completion,
            "series": series_list
        } 