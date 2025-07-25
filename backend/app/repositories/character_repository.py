"""
Character repository for data access operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.character import Character, CharacterStatus
from app.repositories.base import BaseRepository


class CharacterRepository(BaseRepository[Character]):
    """Repository for Character model operations."""
    
    def __init__(self, db: Session):
        super().__init__(Character, db)
    
    def get_by_name(self, name: str) -> Optional[Character]:
        """Get character by name."""
        return self.get_by_field("name", name)
    
    def get_by_alias(self, alias: str) -> List[Character]:
        """Get characters by alias."""
        return self.db.query(Character).filter(Character.aliases.contains([alias])).all()
    
    def get_by_world(self, world_id: str) -> List[Character]:
        """Get characters by world of origin."""
        return self.get_by_field_multi("world_of_origin_id", world_id)
    
    def get_by_species(self, species: str) -> List[Character]:
        """Get characters by species."""
        return self.get_by_field_multi("species", species)
    
    def get_by_status(self, status: CharacterStatus) -> List[Character]:
        """Get characters by status."""
        return self.get_multi(filters={"status": status})
    
    def search_characters(self, search_term: str) -> List[Character]:
        """Search characters by name, aliases, and biography."""
        # Search in name and biography
        name_bio_results = self.search(search_term, ["name", "biography"])
        
        # Search in aliases
        alias_results = self.db.query(Character).filter(
            Character.aliases.any(lambda x: search_term.lower() in x.lower())
        ).all()
        
        # Combine and deduplicate results
        all_results = name_bio_results + alias_results
        seen_ids = set()
        unique_results = []
        
        for char in all_results:
            if char.id not in seen_ids:
                seen_ids.add(char.id)
                unique_results.append(char)
        
        return unique_results
    
    def get_character_with_relationships(self, character_id: str) -> Optional[dict]:
        """Get a character with their relationships."""
        character = self.get(character_id)
        if not character:
            return None
        
        return {
            "character": character,
            "relationships": character.relationships,
            "related_characters": character.related_characters,
            "books": [bc.book for bc in character.books],
            "magic_systems": [cms.magic_system for cms in character.magic_systems]
        }
    
    def get_characters_by_magic_system(self, magic_system_id: str) -> List[Character]:
        """Get characters that use a specific magic system."""
        return self.db.query(Character).join(Character.magic_systems).filter(
            Character.magic_systems.any(magic_system_id=magic_system_id)
        ).all()
    
    def get_characters_in_book(self, book_id: str) -> List[Character]:
        """Get characters that appear in a specific book."""
        return self.db.query(Character).join(Character.books).filter(
            Character.books.any(book_id=book_id)
        ).all()
    
    def get_pov_characters(self) -> List[Character]:
        """Get characters who are POV characters in any book."""
        return self.db.query(Character).join(Character.books).filter(
            Character.books.any(is_pov_character=True)
        ).distinct().all() 