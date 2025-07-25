"""
Magic System service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.repositories.magic_system_repository import MagicSystemRepository
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class MagicSystemService(BaseService[MagicSystemRepository]):
    """Service for Magic System business logic."""
    
    def __init__(self, repository: MagicSystemRepository):
        super().__init__(repository)
    
    def get_magic_system_by_name(self, name: str) -> Optional[Any]:
        """Get magic system by name."""
        return self.repository.get_by_name(name)
    
    def get_magic_systems_by_world(self, world_id: str) -> List[Any]:
        """Get magic systems by world."""
        return self.repository.get_by_world(world_id)
    
    def get_investiture_based(self) -> List[Any]:
        """Get investiture-based magic systems."""
        return self.repository.get_investiture_based()
    
    def search_magic_systems(self, search_term: str) -> List[Any]:
        """Search magic systems by name and description."""
        return self.repository.search_magic_systems(search_term)
    
    def get_magic_system_with_users(self, magic_system_id: str) -> Optional[Dict[str, Any]]:
        """Get a magic system with its users."""
        return self.repository.get_magic_system_with_users(magic_system_id)
    
    def get_magic_systems_by_world_with_stats(self, world_id: str) -> List[Dict[str, Any]]:
        """Get all magic systems for a world with user counts."""
        return self.repository.get_magic_systems_by_world(world_id)
    
    def get_magic_systems_overview(self) -> Dict[str, Any]:
        """Get an overview of all magic systems with statistics."""
        magic_systems = self.get_multi()
        
        total_magic_systems = len(magic_systems)
        investiture_based = len([ms for ms in magic_systems if ms.is_investiture_based])
        
        # Group by world
        magic_systems_by_world = {}
        for ms in magic_systems:
            world_name = ms.world.name if ms.world else "Unknown"
            if world_name not in magic_systems_by_world:
                magic_systems_by_world[world_name] = 0
            magic_systems_by_world[world_name] += 1
        
        # Calculate average users per magic system
        total_users = sum(len(ms.users) for ms in magic_systems)
        avg_users = total_users / total_magic_systems if total_magic_systems > 0 else 0
        
        return {
            "total_magic_systems": total_magic_systems,
            "investiture_based": investiture_based,
            "non_investiture_based": total_magic_systems - investiture_based,
            "magic_systems_by_world": magic_systems_by_world,
            "total_users": total_users,
            "average_users_per_system": avg_users,
            "magic_systems": magic_systems
        } 