"""
Search service for cross-entity search functionality.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories import (
    WorldRepository, SeriesRepository, BookRepository, 
    CharacterRepository, MagicSystemRepository, ShardRepository
)
import logging

logger = logging.getLogger(__name__)


class SearchService:
    """Service for cross-entity search functionality."""
    
    def __init__(self, db: Session):
        self.db = db
        self.world_repo = WorldRepository(db)
        self.series_repo = SeriesRepository(db)
        self.book_repo = BookRepository(db)
        self.character_repo = CharacterRepository(db)
        self.magic_system_repo = MagicSystemRepository(db)
        self.shard_repo = ShardRepository(db)
    
    def search_all(self, search_term: str, limit_per_type: int = 10) -> Dict[str, List[Any]]:
        """Search across all entity types."""
        results = {
            "worlds": self.world_repo.search_worlds(search_term)[:limit_per_type],
            "series": self.series_repo.search_series(search_term)[:limit_per_type],
            "books": self.book_repo.search_books(search_term)[:limit_per_type],
            "characters": self.character_repo.search_characters(search_term)[:limit_per_type],
            "magic_systems": self.magic_system_repo.search_magic_systems(search_term)[:limit_per_type],
            "shards": self.shard_repo.search_shards(search_term)[:limit_per_type]
        }
        
        # Add result counts
        total_results = sum(len(results[key]) for key in results)
        results["total_results"] = total_results
        results["search_term"] = search_term
        
        return results
    
    def search_by_type(self, search_term: str, entity_type: str, limit: int = 50) -> List[Any]:
        """Search within a specific entity type."""
        search_methods = {
            "worlds": self.world_repo.search_worlds,
            "series": self.series_repo.search_series,
            "books": self.book_repo.search_books,
            "characters": self.character_repo.search_characters,
            "magic_systems": self.magic_system_repo.search_magic_systems,
            "shards": self.shard_repo.search_shards
        }
        
        if entity_type not in search_methods:
            return []
        
        return search_methods[entity_type](search_term)[:limit]
    
    def get_search_suggestions(self, search_term: str, limit: int = 10) -> List[str]:
        """Get search suggestions based on partial input."""
        suggestions = set()
        
        # Search across all entities and collect names/titles
        all_results = self.search_all(search_term, limit_per_type=limit)
        
        for entity_type, results in all_results.items():
            if entity_type in ["total_results", "search_term"]:
                continue
            
            for result in results:
                if hasattr(result, 'name'):
                    suggestions.add(result.name)
                elif hasattr(result, 'title'):
                    suggestions.add(result.title)
        
        # Sort by relevance (exact matches first)
        sorted_suggestions = sorted(
            list(suggestions),
            key=lambda x: (not x.lower().startswith(search_term.lower()), x.lower())
        )
        
        return sorted_suggestions[:limit]
    
    def advanced_search(
        self, 
        search_term: str = None,
        entity_types: List[str] = None,
        filters: Dict[str, Any] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """Advanced search with filters and entity type selection."""
        if entity_types is None:
            entity_types = ["worlds", "series", "books", "characters", "magic_systems", "shards"]
        
        results = {}
        
        for entity_type in entity_types:
            if entity_type == "worlds":
                results[entity_type] = self._filter_worlds(
                    self.world_repo.search_worlds(search_term) if search_term else self.world_repo.get_multi(),
                    filters
                )[:limit]
            elif entity_type == "series":
                results[entity_type] = self._filter_series(
                    self.series_repo.search_series(search_term) if search_term else self.series_repo.get_multi(),
                    filters
                )[:limit]
            elif entity_type == "books":
                results[entity_type] = self._filter_books(
                    self.book_repo.search_books(search_term) if search_term else self.book_repo.get_multi(),
                    filters
                )[:limit]
            elif entity_type == "characters":
                results[entity_type] = self._filter_characters(
                    self.character_repo.search_characters(search_term) if search_term else self.character_repo.get_multi(),
                    filters
                )[:limit]
            elif entity_type == "magic_systems":
                results[entity_type] = self._filter_magic_systems(
                    self.magic_system_repo.search_magic_systems(search_term) if search_term else self.magic_system_repo.get_multi(),
                    filters
                )[:limit]
            elif entity_type == "shards":
                results[entity_type] = self._filter_shards(
                    self.shard_repo.search_shards(search_term) if search_term else self.shard_repo.get_multi(),
                    filters
                )[:limit]
        
        results["total_results"] = sum(len(results[key]) for key in results if key != "total_results")
        results["search_term"] = search_term
        results["filters"] = filters
        
        return results
    
    def _filter_worlds(self, worlds: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """Filter worlds based on criteria."""
        if not filters:
            return worlds
        
        filtered = worlds
        
        if "is_habitable" in filters:
            filtered = [w for w in filtered if w.is_habitable == filters["is_habitable"]]
        
        if "system" in filters:
            filtered = [w for w in filtered if w.system == filters["system"]]
        
        return filtered
    
    def _filter_series(self, series: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """Filter series based on criteria."""
        if not filters:
            return series
        
        filtered = series
        
        if "status" in filters:
            filtered = [s for s in filtered if s.status.value == filters["status"]]
        
        if "world_id" in filters:
            filtered = [s for s in filtered if s.world_id == filters["world_id"]]
        
        return filtered
    
    def _filter_books(self, books: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """Filter books based on criteria."""
        if not filters:
            return books
        
        filtered = books
        
        if "is_standalone" in filters:
            filtered = [b for b in filtered if b.is_standalone == filters["is_standalone"]]
        
        if "world_id" in filters:
            filtered = [b for b in filtered if b.world_id == filters["world_id"]]
        
        if "series_id" in filters:
            filtered = [b for b in filtered if b.series_id == filters["series_id"]]
        
        return filtered
    
    def _filter_characters(self, characters: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """Filter characters based on criteria."""
        if not filters:
            return characters
        
        filtered = characters
        
        if "status" in filters:
            filtered = [c for c in filtered if c.status.value == filters["status"]]
        
        if "species" in filters:
            filtered = [c for c in filtered if c.species == filters["species"]]
        
        if "world_id" in filters:
            filtered = [c for c in filtered if c.world_of_origin_id == filters["world_id"]]
        
        return filtered
    
    def _filter_magic_systems(self, magic_systems: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """Filter magic systems based on criteria."""
        if not filters:
            return magic_systems
        
        filtered = magic_systems
        
        if "is_investiture_based" in filters:
            filtered = [ms for ms in filtered if ms.is_investiture_based == filters["is_investiture_based"]]
        
        if "world_id" in filters:
            filtered = [ms for ms in filtered if ms.world_id == filters["world_id"]]
        
        return filtered
    
    def _filter_shards(self, shards: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """Filter shards based on criteria."""
        if not filters:
            return shards
        
        filtered = shards
        
        if "status" in filters:
            filtered = [s for s in filtered if s.status.value == filters["status"]]
        
        if "is_combined" in filters:
            filtered = [s for s in filtered if s.is_combined == filters["is_combined"]]
        
        return filtered
