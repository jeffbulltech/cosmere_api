#!/usr/bin/env python3
"""
Data import script for Cosmere API.
Imports data from JSON files into the database.
"""
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import uuid

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import (
    Base, World, Series, Book, Character, MagicSystem, Shard,
    CharacterRelationship, BookCharacter, CharacterMagicSystem, ShardVessel
)
from app.core.config import settings
import structlog

logger = structlog.get_logger(__name__)


class DataImporter:
    """Data importer for Cosmere data."""
    
    def __init__(self):
        self.db = SessionLocal()
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
    
    def load_json_file(self, filename: str) -> List[Dict[str, Any]]:
        """Load data from a JSON file."""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data)} records from {filename}")
            return data
        except FileNotFoundError:
            logger.warning(f"File {filename} not found, skipping")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing {filename}: {e}")
            return []
    
    def create_worlds(self) -> Dict[str, str]:
        """Create world records and return mapping of names to IDs."""
        worlds_data = self.load_json_file("worlds.json")
        world_mapping = {}
        
        # Create default worlds based on existing data
        default_worlds = [
            {"id": "roshar", "name": "Roshar", "description": "The world of The Stormlight Archive"},
            {"id": "scadrial", "name": "Scadrial", "description": "The world of Mistborn"},
            {"id": "sel", "name": "Sel", "description": "The world of Elantris"},
            {"id": "nalthis", "name": "Nalthis", "description": "The world of Warbreaker"},
            {"id": "first_of_the_sun", "name": "First of the Sun", "description": "The world of Sixth of the Dusk"},
            {"id": "threnody", "name": "Threnody", "description": "The world of Shadows for Silence"},
            {"id": "ashyn", "name": "Ashyn", "description": "The world of The Silence Divine"},
            {"id": "braize", "name": "Braize", "description": "The world of The Stormlight Archive"},
        ]
        
        for world_data in default_worlds:
            world = World(
                id=world_data["id"],
                name=world_data["name"],
                description=world_data["description"]
            )
            self.db.add(world)
            world_mapping[world_data["name"].lower()] = world_data["id"]
        
        self.db.commit()
        logger.info(f"Created {len(default_worlds)} worlds")
        return world_mapping
    
    def create_series(self, world_mapping: Dict[str, str]):
        """Create series records."""
        series_data = self.load_json_file("series.json")
        
        for series_item in series_data:
            world_id = world_mapping.get(series_item.get("world", "").lower())
            
            series = Series(
                id=series_item["id"],
                name=series_item["name"],
                world_id=world_id,
                planned_books=series_item.get("planned_books"),
                current_books=series_item.get("current_books", 0),
                status=series_item.get("status", "ongoing")
            )
            self.db.add(series)
        
        self.db.commit()
        logger.info(f"Created {len(series_data)} series")
    
    def create_books(self, world_mapping: Dict[str, str]):
        """Create book records."""
        books_data = self.load_json_file("books.json")
        
        for book_item in books_data:
            world_id = world_mapping.get(book_item.get("world_id", "").lower())
            
            book = Book(
                id=book_item["id"],
                title=book_item["title"],
                series_id=book_item.get("series_id"),
                world_id=world_id,
                publication_date=None,  # Could parse from string if available
                summary=book_item.get("summary")
            )
            self.db.add(book)
        
        self.db.commit()
        logger.info(f"Created {len(books_data)} books")
    
    def create_characters(self, world_mapping: Dict[str, str]):
        """Create character records."""
        characters_data = self.load_json_file("characters.json")
        
        for char_item in characters_data:
            world_id = world_mapping.get(char_item.get("world_of_origin_id", "").lower())
            
            character = Character(
                id=char_item["id"],
                name=char_item["name"],
                aliases=char_item.get("aliases", []),
                world_of_origin_id=world_id,
                species=char_item.get("species"),
                status=char_item.get("status", "unknown"),
                biography=char_item.get("biography")
            )
            self.db.add(character)
        
        self.db.commit()
        logger.info(f"Created {len(characters_data)} characters")
    
    def create_magic_systems(self, world_mapping: Dict[str, str]):
        """Create magic system records."""
        magic_data = self.load_json_file("magic_systems.json")
        
        for magic_item in magic_data:
            world_id = world_mapping.get(magic_item.get("world_id", "").lower())
            
            magic_system = MagicSystem(
                id=magic_item["id"],
                name=magic_item.get("title", magic_item["id"]),
                world_id=world_id,
                description=magic_item.get("summary")
            )
            self.db.add(magic_system)
        
        self.db.commit()
        logger.info(f"Created {len(magic_data)} magic systems")
    
    def create_shards(self):
        """Create shard records."""
        shards_data = self.load_json_file("shards.json")
        
        for shard_item in shards_data:
            shard = Shard(
                id=shard_item["id"],
                name=shard_item.get("title", shard_item["id"]),
                description=shard_item.get("summary")
            )
            self.db.add(shard)
        
        self.db.commit()
        logger.info(f"Created {len(shards_data)} shards")
    
    def create_book_character_relationships(self):
        """Create book-character relationships based on character appearances."""
        # This is a simplified approach - in a real scenario, you'd have
        # explicit data about which characters appear in which books
        books = self.db.query(Book).all()
        characters = self.db.query(Character).all()
        
        # For now, we'll create some basic relationships
        # In practice, this would come from explicit data
        for book in books:
            # Add some characters to each book (this is placeholder logic)
            for i, character in enumerate(characters[:5]):  # Limit to first 5 characters per book
                book_char = BookCharacter(
                    id=f"{book.id}_{character.id}",
                    book_id=book.id,
                    character_id=character.id,
                    role="supporting" if i > 0 else "main",
                    is_pov_character=(i == 0)
                )
                self.db.add(book_char)
        
        self.db.commit()
        logger.info("Created book-character relationships")
    
    def import_all(self):
        """Import all data."""
        logger.info("Starting data import...")
        
        try:
            # Create worlds first (they're referenced by other entities)
            world_mapping = self.create_worlds()
            
            # Create other entities
            self.create_series(world_mapping)
            self.create_books(world_mapping)
            self.create_characters(world_mapping)
            self.create_magic_systems(world_mapping)
            self.create_shards()
            
            # Create relationships
            self.create_book_character_relationships()
            
            logger.info("Data import completed successfully!")
            
        except Exception as e:
            logger.error(f"Error during data import: {e}")
            self.db.rollback()
            raise


def main():
    """Main function to run the data import."""
    print("🚀 Starting Cosmere data import...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Import data
    with DataImporter() as importer:
        importer.import_all()
    
    print("🎉 Data import completed successfully!")
    print("\nNext steps:")
    print("1. Start the API: uvicorn app.main:app --reload")
    print("2. Access API docs: http://localhost:8000/api/v1/docs")
    print("3. Test endpoints with sample data")


if __name__ == "__main__":
    main() 