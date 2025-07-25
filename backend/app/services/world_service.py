"""
World service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.repositories.world_repository import WorldRepository
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class WorldService(BaseService[WorldRepository]):
    """Service for World business logic."""
    
    def __init__(self, repository: WorldRepository):
        super().__init__(repository)
    
    def get_world_by_name(self, name: str) -> Optional[Any]:
        """Get world by name."""
        return self.repository.get_by_name(name)
    
    def get_worlds_by_system(self, system: str) -> List[Any]:
        """Get worlds by planetary system."""
        return self.repository.get_by_system(system)
    
    def get_habitable_worlds(self) -> List[Any]:
        """Get all habitable worlds."""
        return self.repository.get_habitable_worlds()
    
    def search_worlds(self, search_term: str) -> List[Any]:
        """Search worlds by name and description."""
        return self.repository.search_worlds(search_term)
    
    def get_worlds_with_series(self) -> List[Any]:
        """Get worlds that have series associated with them."""
        return self.repository.get_worlds_with_series()
    
    def get_worlds_with_magic_systems(self) -> List[Any]:
        """Get worlds that have magic systems."""
        return self.repository.get_worlds_with_magic_systems()
    
    def get_world_summary(self, world_id: str) -> Optional[Dict[str, Any]]:
        """Get a comprehensive summary of a world."""
        summary = self.repository.get_world_summary(world_id)
        if not summary:
            return None
        
        # Add additional business logic here
        world = summary["world"]
        
        # Calculate completion percentage for series
        series_completion = 0
        if world.series:
            total_books = sum(len(s.books) for s in world.series)
            planned_books = sum(s.planned_books or 0 for s in world.series)
            if planned_books > 0:
                series_completion = (total_books / planned_books) * 100
        
        return {
            **summary,
            "series_completion_percentage": series_completion,
            "has_magic_systems": len(world.magic_systems) > 0,
            "has_characters": len(world.characters) > 0
        }
    
    def get_worlds_overview(self) -> Dict[str, Any]:
        """Get an overview of all worlds with statistics."""
        worlds = self.get_multi()
        
        total_worlds = len(worlds)
        habitable_worlds = len([w for w in worlds if w.is_habitable])
        worlds_with_series = len([w for w in worlds if w.series])
        worlds_with_magic = len([w for w in worlds if w.magic_systems])
        
        return {
            "total_worlds": total_worlds,
            "habitable_worlds": habitable_worlds,
            "worlds_with_series": worlds_with_series,
            "worlds_with_magic_systems": worlds_with_magic,
            "worlds": worlds
        } 