"""
Character service for business logic operations.
"""
from typing import List, Optional, Dict, Any
from app.repositories.character_repository import CharacterRepository
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class CharacterService(BaseService[CharacterRepository]):
    """Service for Character business logic."""
    
    def __init__(self, repository: CharacterRepository):
        super().__init__(repository)
    
    def get_character_by_name(self, name: str) -> Optional[Any]:
        """Get character by name."""
        return self.repository.get_by_name(name)
    
    def get_characters_by_alias(self, alias: str) -> List[Any]:
        """Get characters by alias."""
        return self.repository.get_by_alias(alias)
    
    def get_characters_by_world(self, world_id: str) -> List[Any]:
        """Get characters by world of origin."""
        return self.repository.get_by_world(world_id)
    
    def get_characters_by_species(self, species: str) -> List[Any]:
        """Get characters by species."""
        return self.repository.get_by_species(species)
    
    def get_characters_by_status(self, status: str) -> List[Any]:
        """Get characters by status."""
        return self.repository.get_by_status(status)
    
    def search_characters(self, search_term: str) -> List[Any]:
        """Search characters by name, aliases, and biography."""
        return self.repository.search_characters(search_term)
    
    def get_character_with_relationships(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get a character with their relationships."""
        return self.repository.get_character_with_relationships(character_id)
    
    def get_characters_by_magic_system(self, magic_system_id: str) -> List[Any]:
        """Get characters that use a specific magic system."""
        return self.repository.get_characters_by_magic_system(magic_system_id)
    
    def get_characters_in_book(self, book_id: str) -> List[Any]:
        """Get characters that appear in a specific book."""
        return self.repository.get_characters_in_book(book_id)
    
    def get_pov_characters(self) -> List[Any]:
        """Get characters who are POV characters in any book."""
        return self.repository.get_pov_characters()
    
    def get_character_overview(self) -> Dict[str, Any]:
        """Get an overview of all characters with statistics."""
        characters = self.get_multi()
        
        total_characters = len(characters)
        
        # Group by world
        characters_by_world = {}
        for char in characters:
            world_name = char.world_of_origin.name if char.world_of_origin else "Unknown"
            if world_name not in characters_by_world:
                characters_by_world[world_name] = 0
            characters_by_world[world_name] += 1
        
        # Group by species
        characters_by_species = {}
        for char in characters:
            species = char.species or "Unknown"
            if species not in characters_by_species:
                characters_by_species[species] = 0
            characters_by_species[species] += 1
        
        # Group by status
        characters_by_status = {}
        for char in characters:
            status = char.status.value if char.status else "unknown"
            if status not in characters_by_status:
                characters_by_status[status] = 0
            characters_by_status[status] += 1
        
        return {
            "total_characters": total_characters,
            "characters_by_world": characters_by_world,
            "characters_by_species": characters_by_species,
            "characters_by_status": characters_by_status,
            "characters": characters
        }
    
    def get_character_network(self, character_id: str) -> Optional[Dict[str, Any]]:
        """Get character relationship network."""
        character_data = self.get_character_with_relationships(character_id)
        if not character_data:
            return None
        
        character = character_data["character"]
        relationships = character_data["relationships"]
        
        # Build network data
        nodes = [{"id": character.id, "name": character.name, "type": "main"}]
        edges = []
        
        for rel in relationships:
            related_char = rel.related_character
            nodes.append({
                "id": related_char.id,
                "name": related_char.name,
                "type": "related"
            })
            edges.append({
                "source": character.id,
                "target": related_char.id,
                "type": rel.relationship_type.value,
                "description": rel.description
            })
        
        return {
            "character": character,
            "network": {
                "nodes": nodes,
                "edges": edges
            }
        } 