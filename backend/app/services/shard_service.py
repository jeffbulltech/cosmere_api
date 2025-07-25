"""
Shard service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.repositories.shard_repository import ShardRepository
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class ShardService(BaseService[ShardRepository]):
    """Service for Shard business logic."""
    
    def __init__(self, repository: ShardRepository):
        super().__init__(repository)
    
    def get_shard_by_name(self, name: str) -> Optional[Any]:
        """Get shard by name."""
        return self.repository.get_by_name(name)
    
    def get_shards_by_intent(self, intent: str) -> List[Any]:
        """Get shards by intent."""
        return self.repository.get_by_intent(intent)
    
    def get_shards_by_status(self, status: str) -> List[Any]:
        """Get shards by status."""
        return self.repository.get_by_status(status)
    
    def get_whole_shards(self) -> List[Any]:
        """Get whole (un-splintered) shards."""
        return self.repository.get_whole_shards()
    
    def get_splintered_shards(self) -> List[Any]:
        """Get splintered shards."""
        return self.repository.get_splintered_shards()
    
    def get_combined_shards(self) -> List[Any]:
        """Get combined shards."""
        return self.repository.get_combined_shards()
    
    def search_shards(self, search_term: str) -> List[Any]:
        """Search shards by name, intent, and description."""
        return self.repository.search_shards(search_term)
    
    def get_shard_with_vessels(self, shard_id: str) -> Optional[Dict[str, Any]]:
        """Get a shard with its vessels."""
        return self.repository.get_shard_with_vessels(shard_id)
    
    def get_shards_by_vessel(self, vessel_name: str) -> List[Any]:
        """Get shards by vessel name."""
        return self.repository.get_shards_by_vessel(vessel_name)
    
    def get_shards_overview(self) -> Dict[str, Any]:
        """Get an overview of all shards with statistics."""
        shards = self.get_multi()
        
        total_shards = len(shards)
        whole_shards = len([s for s in shards if s.status.value == "whole"])
        splintered_shards = len([s for s in shards if s.status.value == "splintered"])
        combined_shards = len([s for s in shards if s.is_combined])
        
        # Group by status
        shards_by_status = {}
        for shard in shards:
            status = shard.status.value
            if status not in shards_by_status:
                shards_by_status[status] = 0
            shards_by_status[status] += 1
        
        # Calculate vessels statistics
        total_vessels = sum(len(shard.vessels) for shard in shards)
        avg_vessels = total_vessels / total_shards if total_shards > 0 else 0
        
        return {
            "total_shards": total_shards,
            "whole_shards": whole_shards,
            "splintered_shards": splintered_shards,
            "combined_shards": combined_shards,
            "shards_by_status": shards_by_status,
            "total_vessels": total_vessels,
            "average_vessels_per_shard": avg_vessels,
            "shards": shards
        } 