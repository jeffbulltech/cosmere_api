"""
Dependency injection for API endpoints.
"""
from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends

from app.core.database import get_db
from app.repositories import (
    WorldRepository, SeriesRepository, BookRepository, CharacterRepository,
    MagicSystemRepository, ShardRepository
)
from app.services import (
    WorldService, BookService, CharacterService, SeriesService,
    MagicSystemService, ShardService, SearchService
)
from app.services.cache_service import cache_service


# Repository dependencies
def get_world_repository(db: Session = Depends(get_db)) -> WorldRepository:
    """Get world repository."""
    return WorldRepository(db)


def get_series_repository(db: Session = Depends(get_db)) -> SeriesRepository:
    """Get series repository."""
    return SeriesRepository(db)


def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    """Get book repository."""
    return BookRepository(db)


def get_character_repository(db: Session = Depends(get_db)) -> CharacterRepository:
    """Get character repository."""
    return CharacterRepository(db)


def get_magic_system_repository(db: Session = Depends(get_db)) -> MagicSystemRepository:
    """Get magic system repository."""
    return MagicSystemRepository(db)


def get_shard_repository(db: Session = Depends(get_db)) -> ShardRepository:
    """Get shard repository."""
    return ShardRepository(db)


# Service dependencies
def get_world_service(
    repository: WorldRepository = Depends(get_world_repository)
) -> WorldService:
    """Get world service."""
    return WorldService(repository)


def get_series_service(
    repository: SeriesRepository = Depends(get_series_repository)
) -> SeriesService:
    """Get series service."""
    return SeriesService(repository)


def get_book_service(
    repository: BookRepository = Depends(get_book_repository)
) -> BookService:
    """Get book service."""
    return BookService(repository)


def get_character_service(
    repository: CharacterRepository = Depends(get_character_repository)
) -> CharacterService:
    """Get character service."""
    return CharacterService(repository)


def get_magic_system_service(
    repository: MagicSystemRepository = Depends(get_magic_system_repository)
) -> MagicSystemService:
    """Get magic system service."""
    return MagicSystemService(repository)


def get_shard_service(
    repository: ShardRepository = Depends(get_shard_repository)
) -> ShardService:
    """Get shard service."""
    return ShardService(repository)


def get_search_service(db: Session = Depends(get_db)) -> SearchService:
    """Get search service."""
    return SearchService(db)


def get_cache_service():
    """Get cache service."""
    return cache_service
