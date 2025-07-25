"""
Unit tests for repository layer.
"""
import pytest
from sqlalchemy.orm import Session
from app.repositories import (
    WorldRepository, SeriesRepository, BookRepository, CharacterRepository,
    MagicSystemRepository, ShardRepository
)
from app.models import World, Series, Book, Character, MagicSystem, Shard


class TestWorldRepository:
    """Test cases for WorldRepository."""
    
    def test_create_world(self, db_session: Session, sample_world_data: dict):
        """Test creating a world."""
        repo = WorldRepository(db_session)
        world = repo.create(sample_world_data)
        
        assert world is not None
        assert world.id == sample_world_data["id"]
        assert world.name == sample_world_data["name"]
        assert world.description == sample_world_data["description"]
    
    def test_get_world(self, db_session: Session, sample_world_data: dict):
        """Test getting a world by ID."""
        repo = WorldRepository(db_session)
        created_world = repo.create(sample_world_data)
        
        world = repo.get(created_world.id)
        assert world is not None
        assert world.id == created_world.id
        assert world.name == created_world.name
    
    def test_get_world_not_found(self, db_session: Session):
        """Test getting a non-existent world."""
        repo = WorldRepository(db_session)
        world = repo.get("non-existent")
        assert world is None
    
    def test_get_multi_worlds(self, db_session: Session, sample_world_data: dict):
        """Test getting multiple worlds."""
        repo = WorldRepository(db_session)
        
        # Create multiple worlds
        world1_data = sample_world_data.copy()
        world1_data["id"] = "roshar"
        world1_data["name"] = "Roshar"
        
        world2_data = sample_world_data.copy()
        world2_data["id"] = "scadrial"
        world2_data["name"] = "Scadrial"
        
        repo.create(world1_data)
        repo.create(world2_data)
        
        worlds = repo.get_multi()
        assert len(worlds) == 2
        assert any(w.name == "Roshar" for w in worlds)
        assert any(w.name == "Scadrial" for w in worlds)
    
    def test_update_world(self, db_session: Session, sample_world_data: dict):
        """Test updating a world."""
        repo = WorldRepository(db_session)
        world = repo.create(sample_world_data)
        
        update_data = {"description": "Updated description"}
        updated_world = repo.update(world.id, update_data)
        
        assert updated_world is not None
        assert updated_world.description == "Updated description"
    
    def test_delete_world(self, db_session: Session, sample_world_data: dict):
        """Test deleting a world."""
        repo = WorldRepository(db_session)
        world = repo.create(sample_world_data)
        
        success = repo.delete(world.id)
        assert success is True
        
        # Verify world is deleted
        deleted_world = repo.get(world.id)
        assert deleted_world is None
    
    def test_search_worlds(self, db_session: Session, sample_world_data: dict):
        """Test searching worlds."""
        repo = WorldRepository(db_session)
        world = repo.create(sample_world_data)
        
        results = repo.search_worlds("Roshar")
        assert len(results) == 1
        assert results[0].id == world.id
    
    def test_get_world_by_name(self, db_session: Session, sample_world_data: dict):
        """Test getting world by name."""
        repo = WorldRepository(db_session)
        world = repo.create(sample_world_data)
        
        found_world = repo.get_by_name("Roshar")
        assert found_world is not None
        assert found_world.id == world.id


class TestSeriesRepository:
    """Test cases for SeriesRepository."""
    
    def test_create_series(self, db_session: Session, sample_series_data: dict):
        """Test creating a series."""
        repo = SeriesRepository(db_session)
        series = repo.create(sample_series_data)
        
        assert series is not None
        assert series.id == sample_series_data["id"]
        assert series.name == sample_series_data["name"]
    
    def test_get_series_by_world(self, db_session: Session, sample_series_data: dict):
        """Test getting series by world."""
        repo = SeriesRepository(db_session)
        series = repo.create(sample_series_data)
        
        world_series = repo.get_by_world("roshar")
        assert len(world_series) == 1
        assert world_series[0].id == series.id
    
    def test_get_ongoing_series(self, db_session: Session, sample_series_data: dict):
        """Test getting ongoing series."""
        repo = SeriesRepository(db_session)
        series = repo.create(sample_series_data)
        
        ongoing = repo.get_ongoing_series()
        assert len(ongoing) == 1
        assert ongoing[0].id == series.id


class TestBookRepository:
    """Test cases for BookRepository."""
    
    def test_create_book(self, db_session: Session, sample_book_data: dict):
        """Test creating a book."""
        repo = BookRepository(db_session)
        book = repo.create(sample_book_data)
        
        assert book is not None
        assert book.id == sample_book_data["id"]
        assert book.title == sample_book_data["title"]
    
    def test_get_books_by_series(self, db_session: Session, sample_book_data: dict):
        """Test getting books by series."""
        repo = BookRepository(db_session)
        book = repo.create(sample_book_data)
        
        series_books = repo.get_by_series("stormlight-archive")
        assert len(series_books) == 1
        assert series_books[0].id == book.id
    
    def test_get_standalone_books(self, db_session: Session, sample_book_data: dict):
        """Test getting standalone books."""
        repo = BookRepository(db_session)
        
        # Create a standalone book
        standalone_data = sample_book_data.copy()
        standalone_data["id"] = "standalone-book"
        standalone_data["title"] = "Standalone Book"
        standalone_data["is_standalone"] = True
        standalone_data["series_id"] = None
        
        book = repo.create(standalone_data)
        
        standalone_books = repo.get_standalone_books()
        assert len(standalone_books) == 1
        assert standalone_books[0].id == book.id


class TestCharacterRepository:
    """Test cases for CharacterRepository."""
    
    def test_create_character(self, db_session: Session, sample_character_data: dict):
        """Test creating a character."""
        repo = CharacterRepository(db_session)
        character = repo.create(sample_character_data)
        
        assert character is not None
        assert character.id == sample_character_data["id"]
        assert character.name == sample_character_data["name"]
    
    def test_get_characters_by_world(self, db_session: Session, sample_character_data: dict):
        """Test getting characters by world."""
        repo = CharacterRepository(db_session)
        character = repo.create(sample_character_data)
        
        world_characters = repo.get_by_world("roshar")
        assert len(world_characters) == 1
        assert world_characters[0].id == character.id
    
    def test_get_characters_by_species(self, db_session: Session, sample_character_data: dict):
        """Test getting characters by species."""
        repo = CharacterRepository(db_session)
        character = repo.create(sample_character_data)
        
        human_characters = repo.get_by_species("Human")
        assert len(human_characters) == 1
        assert human_characters[0].id == character.id


class TestMagicSystemRepository:
    """Test cases for MagicSystemRepository."""
    
    def test_create_magic_system(self, db_session: Session, sample_magic_system_data: dict):
        """Test creating a magic system."""
        repo = MagicSystemRepository(db_session)
        magic_system = repo.create(sample_magic_system_data)
        
        assert magic_system is not None
        assert magic_system.id == sample_magic_system_data["id"]
        assert magic_system.name == sample_magic_system_data["name"]
    
    def test_get_magic_systems_by_world(self, db_session: Session, sample_magic_system_data: dict):
        """Test getting magic systems by world."""
        repo = MagicSystemRepository(db_session)
        magic_system = repo.create(sample_magic_system_data)
        
        world_magic_systems = repo.get_by_world("roshar")
        assert len(world_magic_systems) == 1
        assert world_magic_systems[0].id == magic_system.id
    
    def test_get_investiture_based(self, db_session: Session, sample_magic_system_data: dict):
        """Test getting investiture-based magic systems."""
        repo = MagicSystemRepository(db_session)
        magic_system = repo.create(sample_magic_system_data)
        
        investiture_based = repo.get_investiture_based()
        assert len(investiture_based) == 1
        assert investiture_based[0].id == magic_system.id


class TestShardRepository:
    """Test cases for ShardRepository."""
    
    def test_create_shard(self, db_session: Session, sample_shard_data: dict):
        """Test creating a shard."""
        repo = ShardRepository(db_session)
        shard = repo.create(sample_shard_data)
        
        assert shard is not None
        assert shard.id == sample_shard_data["id"]
        assert shard.name == sample_shard_data["name"]
    
    def test_get_shards_by_intent(self, db_session: Session, sample_shard_data: dict):
        """Test getting shards by intent."""
        repo = ShardRepository(db_session)
        shard = repo.create(sample_shard_data)
        
        honor_shards = repo.get_by_intent("Honor")
        assert len(honor_shards) == 1
        assert honor_shards[0].id == shard.id
    
    def test_get_whole_shards(self, db_session: Session, sample_shard_data: dict):
        """Test getting whole shards."""
        repo = ShardRepository(db_session)
        
        # Create a whole shard
        whole_shard_data = sample_shard_data.copy()
        whole_shard_data["id"] = "whole-shard"
        whole_shard_data["name"] = "Whole Shard"
        whole_shard_data["status"] = "whole"
        
        shard = repo.create(whole_shard_data)
        
        whole_shards = repo.get_whole_shards()
        assert len(whole_shards) == 1
        assert whole_shards[0].id == shard.id 