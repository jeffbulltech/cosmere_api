"""
World repository for data access operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.world import World
from app.repositories.base import BaseRepository


class WorldRepository(BaseRepository[World]):
    """Repository for World model operations."""
    
    def __init__(self, db: Session):
        super().__init__(World, db)
    
    def get_by_name(self, name: str) -> Optional[World]:
        """Get world by name."""
        return self.get_by_field("name", name)
    
    def get_by_system(self, system: str) -> List[World]:
        """Get worlds by planetary system."""
        return self.get_by_field_multi("system", system)
    
    def get_habitable_worlds(self) -> List[World]:
        """Get all habitable worlds."""
        return self.get_multi(filters={"is_habitable": True})
    
    def search_worlds(self, search_term: str) -> List[World]:
        """Search worlds by name and description."""
        return self.search(search_term, ["name", "description"])
    
    def get_worlds_with_series(self) -> List[World]:
        """Get worlds that have series associated with them."""
        return self.db.query(World).filter(World.series.any()).all()
    
    def get_worlds_with_magic_systems(self) -> List[World]:
        """Get worlds that have magic systems."""
        return self.db.query(World).filter(World.magic_systems.any()).all()
    
    def get_world_summary(self, world_id: str) -> Optional[dict]:
        """Get a summary of a world with related counts."""
        world = self.get(world_id)
        if not world:
            return None
        
        return {
            "world": world,
            "series_count": len(world.series),
            "books_count": len(world.books),
            "characters_count": len(world.characters),
            "magic_systems_count": len(world.magic_systems)
        } 