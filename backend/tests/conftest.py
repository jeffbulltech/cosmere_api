"""
Pytest configuration and fixtures for testing.
"""
import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings
from app.models import (
    World, Series, Book, Character, MagicSystem, Shard,
    CharacterRelationship, BookCharacter, CharacterMagicSystem
)


# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine."""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create test database session."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """Create test client with database session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_world_data() -> Dict[str, Any]:
    """Sample world data for testing."""
    return {
        "id": "roshar",
        "name": "Roshar",
        "description": "A world of stone and storms",
        "system": "Rosharan System",
        "is_habitable": True,
        "magic_systems_description": "Surgebinding and Voidbinding",
        "notable_features": "Highstorms, spren, and the Shattered Plains"
    }


@pytest.fixture
def sample_series_data() -> Dict[str, Any]:
    """Sample series data for testing."""
    return {
        "id": "stormlight-archive",
        "name": "The Stormlight Archive",
        "description": "Epic fantasy series on Roshar",
        "world_id": "roshar",
        "planned_books": 10,
        "current_books": 4,
        "status": "ongoing",
        "reading_order": "Primary series"
    }


@pytest.fixture
def sample_book_data() -> Dict[str, Any]:
    """Sample book data for testing."""
    return {
        "id": "way-of-kings",
        "title": "The Way of Kings",
        "series_id": "stormlight-archive",
        "world_id": "roshar",
        "publication_date": "2010-08-31",
        "summary": "The first book in The Stormlight Archive",
        "page_count": 1007,
        "is_standalone": False,
        "reading_order": 1
    }


@pytest.fixture
def sample_character_data() -> Dict[str, Any]:
    """Sample character data for testing."""
    return {
        "id": "kaladin-stormblessed",
        "name": "Kaladin Stormblessed",
        "aliases": ["Kal", "Stormblessed"],
        "world_of_origin_id": "roshar",
        "species": "Human",
        "status": "alive",
        "biography": "A former slave who becomes a Windrunner",
        "appearance": "Dark hair, dark eyes, athletic build",
        "personality": "Honorable, protective, brooding",
        "abilities": "Surgebinding (Windrunner), Shardblade, Shardplate"
    }


@pytest.fixture
def sample_magic_system_data() -> Dict[str, Any]:
    """Sample magic system data for testing."""
    return {
        "id": "surgebinding",
        "name": "Surgebinding",
        "world_id": "roshar",
        "description": "Magic system based on the Ten Surges",
        "mechanics": "Uses Stormlight to power abilities",
        "requirements": "Bond with a spren",
        "limitations": "Requires Stormlight to function",
        "is_investiture_based": True,
        "related_systems": "Voidbinding, Old Magic"
    }


@pytest.fixture
def sample_shard_data() -> Dict[str, Any]:
    """Sample shard data for testing."""
    return {
        "id": "honor",
        "name": "Honor",
        "intent": "Honor",
        "status": "splintered",
        "current_vessel": "None",
        "original_vessel": "Tanavast",
        "description": "The Shard of Honor",
        "perpendicularity": "Stormfather",
        "magic_systems": "Surgebinding",
        "residence": "Roshar",
        "is_combined": False
    }


@pytest.fixture
def populated_db(db_session, sample_world_data, sample_series_data, 
                sample_book_data, sample_character_data, 
                sample_magic_system_data, sample_shard_data):
    """Create a database with sample data."""
    # Create world
    world = World(**sample_world_data)
    db_session.add(world)
    
    # Create series
    series = Series(**sample_series_data)
    db_session.add(series)
    
    # Create book
    book = Book(**sample_book_data)
    db_session.add(book)
    
    # Create character
    character = Character(**sample_character_data)
    db_session.add(character)
    
    # Create magic system
    magic_system = MagicSystem(**sample_magic_system_data)
    db_session.add(magic_system)
    
    # Create shard
    shard = Shard(**sample_shard_data)
    db_session.add(shard)
    
    db_session.commit()
    
    return {
        "world": world,
        "series": series,
        "book": book,
        "character": character,
        "magic_system": magic_system,
        "shard": shard
    } 