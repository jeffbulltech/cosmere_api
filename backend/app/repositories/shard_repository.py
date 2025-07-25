"""
Shard repository for data access operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.shard import Shard, ShardStatus
from app.repositories.base import BaseRepository


class ShardRepository(BaseRepository[Shard]):
    """Repository for Shard model operations."""
    
    def __init__(self, db: Session):
        super().__init__(Shard, db)
    
    def get_by_name(self, name: str) -> Optional[Shard]:
        """Get shard by name."""
        return self.get_by_field("name", name)
    
    def get_by_intent(self, intent: str) -> List[Shard]:
        """Get shards by intent."""
        return self.get_by_field_multi("intent", intent)
    
    def get_by_status(self, status: ShardStatus) -> List[Shard]:
        """Get shards by status."""
        return self.get_multi(filters={"status": status})
    
    def get_whole_shards(self) -> List[Shard]:
        """Get whole (un-splintered) shards."""
        return self.get_by_status(ShardStatus.WHOLE)
    
    def get_splintered_shards(self) -> List[Shard]:
        """Get splintered shards."""
        return self.get_by_status(ShardStatus.SPLINTERED)
    
    def get_combined_shards(self) -> List[Shard]:
        """Get combined shards."""
        return self.get_multi(filters={"is_combined": True})
    
    def search_shards(self, search_term: str) -> List[Shard]:
        """Search shards by name, intent, and description."""
        return self.search(search_term, ["name", "intent", "description"])
    
    def get_shard_with_vessels(self, shard_id: str) -> Optional[dict]:
        """Get a shard with its vessels."""
        shard = self.get(shard_id)
        if not shard:
            return None
        
        return {
            "shard": shard,
            "vessels": shard.vessels,
            "current_vessel": next((v for v in shard.vessels if v.vessel_type == "current"), None),
            "original_vessel": next((v for v in shard.vessels if v.vessel_type == "original"), None)
        }
    
    def get_shards_by_vessel(self, vessel_name: str) -> List[Shard]:
        """Get shards by vessel name."""
        return self.db.query(Shard).filter(
            (Shard.current_vessel == vessel_name) |
            (Shard.original_vessel == vessel_name)
        ).all() 