"""
Magic System repository for data access operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.magic_system import MagicSystem
from app.repositories.base import BaseRepository


class MagicSystemRepository(BaseRepository[MagicSystem]):
    """Repository for MagicSystem model operations."""
    
    def __init__(self, db: Session):
        super().__init__(MagicSystem, db)
    
    def get_by_name(self, name: str) -> Optional[MagicSystem]:
        """Get magic system by name."""
        return self.get_by_field("name", name)
    
    def get_by_world(self, world_id: str) -> List[MagicSystem]:
        """Get magic systems by world."""
        return self.get_by_field_multi("world_id", world_id)
    
    def get_investiture_based(self) -> List[MagicSystem]:
        """Get investiture-based magic systems."""
        return self.get_multi(filters={"is_investiture_based": True})
    
    def search_magic_systems(self, search_term: str) -> List[MagicSystem]:
        """Search magic systems by name and description."""
        return self.search(search_term, ["name", "description", "mechanics"])
    
    def get_magic_system_with_users(self, magic_system_id: str) -> Optional[dict]:
        """Get a magic system with its users."""
        magic_system = self.get(magic_system_id)
        if not magic_system:
            return None
        
        return {
            "magic_system": magic_system,
            "users": [cms.character for cms in magic_system.users],
            "active_users": [cms.character for cms in magic_system.users if cms.is_active],
            "world": magic_system.world
        }
    
    def get_magic_systems_by_world(self, world_id: str) -> List[dict]:
        """Get all magic systems for a world with user counts."""
        magic_systems = self.get_by_world(world_id)
        result = []
        
        for ms in magic_systems:
            result.append({
                "magic_system": ms,
                "user_count": len(ms.users),
                "active_user_count": len([u for u in ms.users if u.is_active])
            })
        
        return result 