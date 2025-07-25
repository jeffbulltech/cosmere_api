"""
Unit tests for service layer.
"""
import pytest
from sqlalchemy.orm import Session
from app.services import (
    WorldService, SeriesService, BookService, CharacterService,
    MagicSystemService, ShardService, SearchService
)
from app.repositories import (
    WorldRepository, SeriesRepository, BookRepository, CharacterRepository,
    MagicSystemRepository, ShardRepository
)


class TestWorldService:
    """Test cases for WorldService."""
    
    def test_get_world(self, db_session: Session, sample_world_data: dict):
        """Test getting a world through service."""
        repo = WorldRepository(db_session)
        service = WorldService(repo)
        
        # Create world through repository
        world = repo.create(sample_world_data)
        
        # Get through service
        retrieved_world = service.get(world.id)
        assert retrieved_world is not None
        assert retrieved_world.id == world.id
        assert retrieved_world.name == world.name
    
    def test_create_world(self, db_session: Session, sample_world_data: dict):
        """Test creating a world through service."""
        repo = WorldRepository(db_session)
        service = WorldService(repo)
        
        created_world = service.create(sample_world_data)
        assert created_world is not None
        assert created_world.id == sample_world_data["id"]
        assert created_world.name == sample_world_data["name"]
    
    def test_get_world_by_name(self, db_session: Session, sample_world_data: dict):
        """Test getting world by name through service."""
        repo = WorldRepository(db_session)
        service = WorldService(repo)
        
        # Create world
        world = repo.create(sample_world_data)
        
        # Get by name through service
        found_world = service.get_world_by_name("Roshar")
        assert found_world is not None
        assert found_world.id == world.id
    
    def test_get_habitable_worlds(self, db_session: Session, sample_world_data: dict):
        """Test getting habitable worlds through service."""
        repo = WorldRepository(db_session)
        service = WorldService(repo)
        
        # Create habitable world
        world = repo.create(sample_world_data)
        
        # Create non-habitable world
        non_habitable_data = sample_world_data.copy()
        non_habitable_data["id"] = "non-habitable"
        non_habitable_data["name"] = "Non-Habitable World"
        non_habitable_data["is_habitable"] = False
        repo.create(non_habitable_data)
        
        habitable_worlds = service.get_habitable_worlds()
        assert len(habitable_worlds) == 1
        assert habitable_worlds[0].id == world.id
    
    def test_search_worlds(self, db_session: Session, sample_world_data: dict):
        """Test searching worlds through service."""
        repo = WorldRepository(db_session)
        service = WorldService(repo)
        
        # Create world
        world = repo.create(sample_world_data)
        
        # Search through service
        results = service.search_worlds("Roshar")
        assert len(results) == 1
        assert results[0].id == world.id
    
    def test_get_worlds_overview(self, db_session: Session, sample_world_data: dict):
        """Test getting worlds overview through service."""
        repo = WorldRepository(db_session)
        service = WorldService(repo)
        
        # Create world
        world = repo.create(sample_world_data)
        
        # Get overview through service
        overview = service.get_worlds_overview()
        assert overview is not None
        assert overview["total_worlds"] == 1
        assert overview["habitable_worlds"] == 1


class TestSeriesService:
    """Test cases for SeriesService."""
    
    def test_get_series(self, db_session: Session, sample_series_data: dict):
        """Test getting a series through service."""
        repo = SeriesRepository(db_session)
        service = SeriesService(repo)
        
        # Create series through repository
        series = repo.create(sample_series_data)
        
        # Get through service
        retrieved_series = service.get(series.id)
        assert retrieved_series is not None
        assert retrieved_series.id == series.id
        assert retrieved_series.name == series.name
    
    def test_get_ongoing_series(self, db_session: Session, sample_series_data: dict):
        """Test getting ongoing series through service."""
        repo = SeriesRepository(db_session)
        service = SeriesService(repo)
        
        # Create ongoing series
        series = repo.create(sample_series_data)
        
        # Create completed series
        completed_data = sample_series_data.copy()
        completed_data["id"] = "completed-series"
        completed_data["name"] = "Completed Series"
        completed_data["status"] = "completed"
        repo.create(completed_data)
        
        ongoing_series = service.get_ongoing_series()
        assert len(ongoing_series) == 1
        assert ongoing_series[0].id == series.id
    
    def test_get_series_by_world(self, db_session: Session, sample_series_data: dict):
        """Test getting series by world through service."""
        repo = SeriesRepository(db_session)
        service = SeriesService(repo)
        
        # Create series
        series = repo.create(sample_series_data)
        
        # Get by world through service
        world_series = service.get_series_by_world("roshar")
        assert len(world_series) == 1
        assert world_series[0].id == series.id


class TestBookService:
    """Test cases for BookService."""
    
    def test_get_book(self, db_session: Session, sample_book_data: dict):
        """Test getting a book through service."""
        repo = BookRepository(db_session)
        service = BookService(repo)
        
        # Create book through repository
        book = repo.create(sample_book_data)
        
        # Get through service
        retrieved_book = service.get(book.id)
        assert retrieved_book is not None
        assert retrieved_book.id == book.id
        assert retrieved_book.title == book.title
    
    def test_get_standalone_books(self, db_session: Session, sample_book_data: dict):
        """Test getting standalone books through service."""
        repo = BookRepository(db_session)
        service = BookService(repo)
        
        # Create standalone book
        standalone_data = sample_book_data.copy()
        standalone_data["id"] = "standalone-book"
        standalone_data["title"] = "Standalone Book"
        standalone_data["is_standalone"] = True
        standalone_data["series_id"] = None
        book = repo.create(standalone_data)
        
        # Create series book
        series_book = repo.create(sample_book_data)
        
        standalone_books = service.get_standalone_books()
        assert len(standalone_books) == 1
        assert standalone_books[0].id == book.id
    
    def test_get_books_by_series(self, db_session: Session, sample_book_data: dict):
        """Test getting books by series through service."""
        repo = BookRepository(db_session)
        service = BookService(repo)
        
        # Create book
        book = repo.create(sample_book_data)
        
        # Get by series through service
        series_books = service.get_books_by_series("stormlight-archive")
        assert len(series_books) == 1
        assert series_books[0].id == book.id


class TestCharacterService:
    """Test cases for CharacterService."""
    
    def test_get_character(self, db_session: Session, sample_character_data: dict):
        """Test getting a character through service."""
        repo = CharacterRepository(db_session)
        service = CharacterService(repo)
        
        # Create character through repository
        character = repo.create(sample_character_data)
        
        # Get through service
        retrieved_character = service.get(character.id)
        assert retrieved_character is not None
        assert retrieved_character.id == character.id
        assert retrieved_character.name == character.name
    
    def test_get_characters_by_world(self, db_session: Session, sample_character_data: dict):
        """Test getting characters by world through service."""
        repo = CharacterRepository(db_session)
        service = CharacterService(repo)
        
        # Create character
        character = repo.create(sample_character_data)
        
        # Get by world through service
        world_characters = service.get_characters_by_world("roshar")
        assert len(world_characters) == 1
        assert world_characters[0].id == character.id
    
    def test_get_characters_by_species(self, db_session: Session, sample_character_data: dict):
        """Test getting characters by species through service."""
        repo = CharacterRepository(db_session)
        service = CharacterService(repo)
        
        # Create character
        character = repo.create(sample_character_data)
        
        # Get by species through service
        human_characters = service.get_characters_by_species("Human")
        assert len(human_characters) == 1
        assert human_characters[0].id == character.id


class TestMagicSystemService:
    """Test cases for MagicSystemService."""
    
    def test_get_magic_system(self, db_session: Session, sample_magic_system_data: dict):
        """Test getting a magic system through service."""
        repo = MagicSystemRepository(db_session)
        service = MagicSystemService(repo)
        
        # Create magic system through repository
        magic_system = repo.create(sample_magic_system_data)
        
        # Get through service
        retrieved_magic_system = service.get(magic_system.id)
        assert retrieved_magic_system is not None
        assert retrieved_magic_system.id == magic_system.id
        assert retrieved_magic_system.name == magic_system.name
    
    def test_get_investiture_based(self, db_session: Session, sample_magic_system_data: dict):
        """Test getting investiture-based magic systems through service."""
        repo = MagicSystemRepository(db_session)
        service = MagicSystemService(repo)
        
        # Create investiture-based magic system
        magic_system = repo.create(sample_magic_system_data)
        
        # Create non-investiture-based magic system
        non_investiture_data = sample_magic_system_data.copy()
        non_investiture_data["id"] = "non-investiture"
        non_investiture_data["name"] = "Non-Investiture Magic"
        non_investiture_data["is_investiture_based"] = False
        repo.create(non_investiture_data)
        
        investiture_based = service.get_investiture_based()
        assert len(investiture_based) == 1
        assert investiture_based[0].id == magic_system.id


class TestShardService:
    """Test cases for ShardService."""
    
    def test_get_shard(self, db_session: Session, sample_shard_data: dict):
        """Test getting a shard through service."""
        repo = ShardRepository(db_session)
        service = ShardService(repo)
        
        # Create shard through repository
        shard = repo.create(sample_shard_data)
        
        # Get through service
        retrieved_shard = service.get(shard.id)
        assert retrieved_shard is not None
        assert retrieved_shard.id == shard.id
        assert retrieved_shard.name == shard.name
    
    def test_get_whole_shards(self, db_session: Session, sample_shard_data: dict):
        """Test getting whole shards through service."""
        repo = ShardRepository(db_session)
        service = ShardService(repo)
        
        # Create whole shard
        whole_shard_data = sample_shard_data.copy()
        whole_shard_data["id"] = "whole-shard"
        whole_shard_data["name"] = "Whole Shard"
        whole_shard_data["status"] = "whole"
        shard = repo.create(whole_shard_data)
        
        # Create splintered shard
        splintered_shard = repo.create(sample_shard_data)
        
        whole_shards = service.get_whole_shards()
        assert len(whole_shards) == 1
        assert whole_shards[0].id == shard.id


class TestSearchService:
    """Test cases for SearchService."""
    
    def test_search_all(self, db_session: Session, sample_world_data: dict, 
                       sample_series_data: dict, sample_book_data: dict):
        """Test searching across all entities."""
        service = SearchService(db_session)
        
        # Create test data
        world_repo = WorldRepository(db_session)
        series_repo = SeriesRepository(db_session)
        book_repo = BookRepository(db_session)
        
        world = world_repo.create(sample_world_data)
        series = series_repo.create(sample_series_data)
        book = book_repo.create(sample_book_data)
        
        # Search across all entities
        results = service.search_all("Roshar", limit_per_type=10)
        
        assert results is not None
        assert "worlds" in results
        assert "series" in results
        assert "books" in results
        assert len(results["worlds"]) == 1
        assert results["worlds"][0].id == world.id
    
    def test_search_by_type(self, db_session: Session, sample_world_data: dict):
        """Test searching by entity type."""
        service = SearchService(db_session)
        
        # Create test data
        world_repo = WorldRepository(db_session)
        world = world_repo.create(sample_world_data)
        
        # Search by type
        results = service.search_by_type("Roshar", "worlds", limit=10)
        
        assert len(results) == 1
        assert results[0].id == world.id
    
    def test_get_search_suggestions(self, db_session: Session, sample_world_data: dict):
        """Test getting search suggestions."""
        service = SearchService(db_session)
        
        # Create test data
        world_repo = WorldRepository(db_session)
        world = world_repo.create(sample_world_data)
        
        # Get suggestions
        suggestions = service.get_search_suggestions("Ros", limit=10)
        
        assert len(suggestions) == 1
        assert "Roshar" in suggestions 